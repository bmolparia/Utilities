import subprocess as sp
import time

class UnkownJobError(Exception):
	pass

class Jobs(object):

	def __init__(self,arguments):

		self.args = arguments  ## A space separated arguments for the qsub command

	def submit_job(self):

		args = self.args
		# Function to make sure a job has been submitted properly
		retry = 0
		args = ['qsub']+args

        while retry<5:
			p1     = sp.Popen(args,stdout=sp.PIPE)
			StdOut = p1.communicate()
			jobID  = StdOut[0].replace('\n','') 
			print jobID 

			try:
				job_number = int(jobID[0:jobID.index('.')]) #Make sure you have a proper job ID
				retry = 100 #Exit while loop
			except:
				retry += 1
				time.sleep(retry*60) #Sleep for some time and then retry
		return 'jobID'
	    
            

	@staticmethod
	def get_job_status(jobID):
	
		p1 = sp.Popen(['qstat','-f',jobID],stdout=sp.PIPE,stderr=sp.PIPE)

		if 'Unknown Job Id' in p1.stderr.read():
			raise UnkownJobError(jobID)
		else:
			p2 = sp.Popen(['grep','job_state'],stdin = p1.stdout,stdout=sp.PIPE)
			tm = p2.stdout.read()
			try:
				status = tm.split('job_state = ')[1].replace('\n','')
			except IndexError:
				print "Got that stupid error\n"
				print tm

		return status
		
	@staticmethod
	def multiple_jobs_completed(jobList):

		l = len(jobList)
		statuses = []
		
		for i in jobList:
			
			completed = not Jobs.isRunning(i)
			statuses.append(completed)

		return all(statuses)
			
	@staticmethod
	def isRunning(jobID):

		holdsignals = ['R','Q','H']
		
		try:
			status = Jobs.get_job_status(jobID)
			if status in holdsignals:
				return True
			else:
				return False
		except UnkownJobError,e:
			
			## NOTE - You can add an option to return the unknown jobID and maybe delete it	
			return False
	
if __name__ == "__main__":
	
	jobID  = '7357745.garibaldi01-adm.cluster.net' 
	jobIDs = ['7357745.garibaldi01-adm.cluster.net','7357746.garibaldi01-adm.cluster.net','7357716.garibaldi01-adm.cluster.net']
	
	#print Jobs.multiple_jobs_completed(jobIDs)
	print Jobs.isRunning(jobID)

