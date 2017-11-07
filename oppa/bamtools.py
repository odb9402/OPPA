import subprocess

def run(input_bam):
    """

    :param input_bam:
    :return:
    """
    commands = ["bamtools", "split", "-in", input_bam, "-reference"]
    bam_process = subprocess.Popen(commands)
    return bam_process
    # what is the proper command of calling bamtools???
