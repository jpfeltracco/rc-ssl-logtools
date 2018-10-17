import setuptools
import sys
import os
import pathlib
import glob
from subprocess import call
from setuptools.command.build_py import build_py
from setuptools.command.install_lib import install_lib

#  def gen_proto():
    #  # generate protobuf messages
    #  package_root_path = os.path.dirname(os.path.realpath(__file__))
    #  proto_path = os.path.join(package_root_path, "ssl_protos")
    #  # note: protoc will create necessary sub dirs to go into proto dir
    #  gen_path = package_root_path

    #  proto_paths = glob.glob(os.path.join(proto_path, "rc_ssl_logtools/proto/*.proto"))
    #  proto_paths = glob.glob("ssl_protos/rc_ssl_logtools/proto/*.proto")

    #  # get only the literal file names, ie "messages_robocup_ssl_geometry.proto"
    #  proto_filenames = ["rc_ssl_logtools/proto/" + os.path.split(path)[1] for path in proto_paths]

    #  # turn into space separated list of proto files
    #  proto_str_list = " ".join(proto_filenames)

    #  cmd_template = "protoc --proto_path={} --python_out={} {}"
    #  cmd = cmd_template.format(proto_path, gen_path, proto_str_list)

    #  # Create build dir if it doesn't exist
    #  pathlib.Path(gen_path).mkdir(exist_ok=True)

    #  print(cmd)

    #  cmd_list = cmd.split(" ")
    #  # finally run protoc command that was built
    #  call(cmd_list)

if __name__ == "__main__":
    #  gen_proto()

    with open("README.md", "r") as fh:
        long_description = fh.read()

    setuptools.setup(
        name="rc_ssl_logtools",
        version="0.0.4",
        author="Jeremy Feltracco",
        author_email="jpfeltracco@gmail.com",
        description="Tools to convert SSL logs to usable Python formats",
        package_data={},
        install_requires=[
            "protobuf",
        ],
        scripts=["bin/ssldump"],
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/jpfeltracco/rc-ssl-logtools",
        packages=['rc_ssl_logtools', 'rc_ssl_logtools.proto'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )


