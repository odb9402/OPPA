from subprocess import call

def run(input_bam):
    commands = ["bamtools", "split", "-in", input_bam, "-reference"]
    call(commands)
