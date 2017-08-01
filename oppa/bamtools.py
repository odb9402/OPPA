import subprocess

def run(input_bam):
    commands = ["bamtools", "split", "-in", input_bam, "-reference"]
    bam_process = subprocess.Popen(commands)
    return bam_process
    # what is the proper command of calling bamtools???
