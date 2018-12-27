import gzip as gz
import zlib
import sys
import time
import struct
import copy

from collections import OrderedDict

from google.protobuf.message import DecodeError

from rc_ssl_logtools.proto.messages_robocup_ssl_referee_pb2 import SSL_Referee as Referee
from rc_ssl_logtools.proto.messages_robocup_ssl_wrapper_pb2 import SSL_WrapperPacket

# From http://wiki.robocup.org/Small_Size_League/Game_Logs
MESSAGE_BLANK = 0  # (ignore message)
MESSAGE_UNKNOWN = 1  # (try to guess message type by parsing the data)
MESSAGE_SSL_VISION_2010 = 2
MESSAGE_SSL_REFBOX_2013 = 3
MESSAGE_SSL_VISION_2014 = 4

def log_frames(ssl_log, start_time=None, duration=None):
    with open(ssl_log, "rb") as f:
        data = f.read()

    z = zlib.decompressobj(15 + 32)
    decomp = z.decompress(data)

    ind = 0

    exp_header = "SSL_LOG_FILE"  # Expected header
    act_header = decomp[ind:ind+len(exp_header)].decode("ascii")
    ind += len(exp_header)

    if exp_header != act_header:
        error_msg = "Error decoding file header, got {}, when expecting {}."
        error_msg = error_msg.format(act_header, exp_header)
        print(error_msg)
        return None

    # message tag
    int_st = struct.Struct(">i")
    log_type_int, = int_st.unpack(decomp[ind:ind+int_st.size])
    ind += int_st.size
     
    # struct containing header information for a given message
    msg_header_st = struct.Struct(">qii")
    msg_header_st_sz = msg_header_st.size

    # first timestamp read from log files
    ts_init = None

    # time to start recording and end recording
    start_time_ns = None if start_time is None else int(start_time * 1e9)
    end_time_ns = None if duration is None else int((start_time + duration) * 1e9)

    vis_pb = SSL_WrapperPacket()
    ref_pb = Referee()

    # protobuf messages pulled from the log
    vis_msgs = []
    ref_msgs = []

    while  ind < len(decomp):
        if (ind + msg_header_st_sz) >= len(decomp):
            break

        ts, tp, sz = msg_header_st.unpack(decomp[ind:ind+msg_header_st_sz])
        ind += msg_header_st_sz

        if (ind + sz) >= len(decomp):
            break

        if ts_init is None:
            ts_init = ts
        dt = ts - ts_init

        msg_str = decomp[ind:ind+sz]
        ind += sz

        if (start_time_ns is None) or (dt > start_time_ns):
            if tp == MESSAGE_SSL_VISION_2014:
                vis_pb.ParseFromString(msg_str)
                if vis_pb.IsInitialized():
                    vis_msgs.append(copy.deepcopy(vis_pb))
                else:
                    print("Failed to parse vision packet!")
            elif tp == MESSAGE_SSL_REFBOX_2013:
                msg_len = ref_pb.ParseFromString(msg_str)
                if ref_pb.IsInitialized():
                    # Why do we keep receiving ref packets with empty log fields???
                    # the sizes of the messages are changing, so why on earth wouldn't
                    # we be seeing any data internally?
                    print(ref_pb.ListFields())
                    ref_msgs.append(copy.deepcopy(ref_pb))
                else:
                    print("Failed to parse referee packet!")
            else:
                print('Not sure what sort of packet I am looking at... Sorry')

            if (end_time_ns is not None) and (dt > end_time_ns): break

    return vis_msgs, ref_msgs
