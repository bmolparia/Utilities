import shlex
import subprocess as sp
import time

class UnkownJobError(Exception):
    pass

def submit_job(args, dependencies=None):
    ''' Function to make sure a job has been submitted properly
    args: a space separated arguments for the qsub command. '''

    if dependencies == None:
        args = 'qsub -m n {}'.format(args)
    else:
        args = 'qsub -m n -W depend=afterok:{1} {0} '.format(args, dependencies)
    args = shlex.split(args)

    retry = 0
    while retry<5:
        p1 = sp.Popen(args, stdout=sp.PIPE)
        StdOut = p1.communicate()
        job_id = StdOut[0].decode('utf-8').replace('\n','')
        print(job_id)

        try:
            # Make sure you have a proper job ID
            job_number = int(job_id[0:job_id.index('.')])
            retry = 100
        except:
            # Sleep for some time and then retry
            retry += 1
            time.sleep(retry*60)
    
    return job_id

def get_job_status(job_id):

    cmd = 'qstat -f {}'.format(job_id)
    cmd = shlex.split(cmd)
    p1 = sp.Popen(cmd,stdout=sp.PIPE,stderr=sp.PIPE)
    p1_err = p1.stderr.read().decode("utf-8")

    if 'Unknown Job Id' in p1_err:
        raise UnkownJobError(job_id)
    else:
        cmd2 = 'grep job_state'
        cmd2 = shlex.split(cmd2)
        p2 = sp.Popen(cmd2, stdin=p1.stdout, stdout=sp.PIPE)
        tm = p2.stdout.read().decode("utf-8")
        try:
            status = tm.split('job_state = ')[1].strip()
        except IndexError:
            print(tm)

    return status

def multiple_jobs_completed(job_list):

    l = len(job_list)
    statuses = []

    for i in job_list:
        completed = not is_running(i)
        statuses.append(completed)

    return all(statuses)

def is_running(job_id):

    holdsignals = ['R','Q','H']

    try:
        status = get_job_status(job_id)
        if status in holdsignals:
            return True
        else:
            return False
    except UnkownJobError as e:
        # NOTE - You can add an option to return the unknown job_id and maybe
        # delete it
        return False

if __name__ == "__main__":

    job_id  = '794264.garibaldi01-adm'
    job_ids = ['7357745.garibaldi01-adm.cluster.net',
    '7357746.garibaldi01-adm.cluster.net','7357716.garibaldi01-adm.cluster.net']

    print(is_running(job_id))
