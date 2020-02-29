# FOR STOP SIGNAL TASK, School study Baseline (gr5)

# Sarah 2020 B&M lab
# **scriptshell modeled from Matt's stroop analysis (on server)**

# skull-stripping scripts are in the server under /scripts


import os,sys
import argparse
import numpy as np
import re
from datetime import datetime
from subprocess import call
from subprocess import check_output
import csv

###Paths (change as needed)

datafolder = "/Volumes/MusicProject/Individual_Projects/Sarah.H/SchoolStudypractice/Functional/Gr5/Baseline"
genericdesign_scrub = "%s/designs/generic_firstlevel_stop_scrub.fsf" %(datafolder)
secondleveldesign = "%sdesigns/secondlevel_design_stop.fsf" %(datafolder)

#set analysis values
numconfounds = 8
smoothmm = 5	#smoothing sigma fwhm in mm
smoothsigma = smoothmm/2.3548	#convert to sigma
additive = 10000	#value added to distinguish brain from background
brightnessthresh = additive * .75
count = 0

groupList = ['Control', 'Music']

for group in groupList:

		subjectDir = "%s/%s/" %(datafolder,group)
		subjectList = [elem for elem in os.listdir(subjectDir) if "." not in elem]
		subjectList.sort()

		for subj in subjectList:
			subject = subj
			subjfolder = subjectDir + subject + "/"
			logfile = subjfolder + "analysis_log.txt"
			checkevfile = subjfolder + "stop_correct_resp_run1.txt"
			finalfile = subjfolder + "secondlevel_cor_stop.gfeat/cope1.feat"

			if os.path.exists(finalfile):
				count = count + 1
				print(count,group,subject,finalfile)

	#Skip this subject if they do not have ev files (hopefully no one!)
			if not os.path.exists(checkevfile):
				print("The subject %s has no EV Files. skipping" %subject)
				continue

			mprage = subjfolder + "mprage.nii.gz"
			brain = subjfolder + "mprage_brain.nii.gz"

# SKULL STRIPPING

			print("###############################")
			print("SKULL STRIPPING COMMENCING")
			print("###############################")
			if not os.path.exists(brain):
		#mprage
				print("Skull Stripping mprage for %s" %subj)
				command = "%sscripts/skullstrip.py %s" %(datafolder,subjfolder)
				print(command)
				call(command,shell = True)

		#field map
				print("Skull stripping field mpa mag for %s" %subj)
				command = "%sscripts/skullstrip_field.py %s" %(datafolder,subjfolder)
				print(command)
				call(command,shell = True)

# Prepare Field Maps
		print("###############################")
		print("preparing field maps for %s" %subj)
		print("###############################")
		fieldmap_phase_file = subjfolder + "fieldmap_phase.nii.gz"
		fieldmap_mag_brain_file = subjfolder + "fieldmap_mag_brain.nii.gz"
		command = "fsl_prepare_fieldmap SIEMENS %s %s fieldmap_phase_rad 2.5" %(fieldmap_phase_file, fieldmap_mag_brain_file)
		call(command, shell = True)
		fieldmap_phase_rad = subjfolder + "fieldmap_phase_rad.nii.gz"

# First Level...

			for run in range(1,3):
				print("we are on run...%d" %run)
				firstlevel_featfolder = subjfolder + "firstlevel_stop_run%d.feat" %(run)
				inputfile = subjfolder + "stop_run%d.nii.gz" %(run)
				designOutput = subjfolder + "firstlevel_stop_design_run%d.fsf" %(run)

	#Scrubbing
				print("###############################")
				print("SCRUB-A-DUB DUBBING")
				print("###############################")
				scrubout = subjfolder + "scrub_confounds_stop_run%d" %(run)
				command = "fsl_motion_outliers -i %s -o %s" %(inputfile, scrubout)

				if not os.path.exists(scrubout):
					print("scrubbing for %s run %d" %(subj, run))
					print(command)
					call(command,shell = True)
					print("i completed scrubbing for %s run %d" %(subj, run))

				else:
					print("scrubbing already done for this one! moving on.")

			print("###############################")
			print("FIRST LEVEL FEAT, COMMENCING")
			print("###############################")

			print("First level FEAT Analysis for: %s, run: %d" %(subject,run))

	# Get number of volumes:

			command = 'fslinfo %s' %(inputfile)
			results = check_output(command,shell=True)
			numtimepoints_1 = results.split()[9]
			numtimepoints = numtimepoints_1.decode()
			print("Number of volumes: %s" %(numtimepoints))

	#set up evfiles
			evfile1 = subjfolder + "go_correct_resp_run%d.txt" %(run)
			evfile2 = subjfolder + "stop_correct_resp_run%d.txt" %(run)
			evfile3 = subjfolder + "go_incorrect_resp_run%d.txt" %(run)
			evfile4 = subjfolder + "stop_incorrect_resp_run%d.txt" %(run)


			command = 'gsed -e "s|DEFINEINPUT|%s|g" -e "s|DEFINEOUTPUT|%s|g" -e "s|DEFINESCRUB|%s|g" -e "s|DEFINEPHASERAD|%s|g" -e "s|DEFINEPHASEMAG|%s|g" -e "s|DEFINESTRUCT|%s|g" -e "s|DEFINEVOLUME|%s|g" -e "s|DEFINEEVFILE1|%s|g" -e "s|DEFINEEVFILE2|%s|g" -e "s|DEFINEEVFILE3|%s|g" -e "s|DEFINEEVFILE4|%s|g" %s>%s' %(re.escape(inputfile),re.escape(firstlevel_featfolder), re.escape(scrubout),re.escape(fieldmap_phase_rad), re.escape(fieldmap_mag_brain_file),re.escape(brain), numtimepoints,re.escape(evfile1),re.escape(evfile2), re.escape(evfile3), re.escape(evfile4),genericdesign_scrub,designOutput)

			call(command, shell = True)
			command = "feat %s" %designOutput
			call(command, shell = True)

			print('i have finished first level feating for %s run: %d' %(subject, run))

### SECOND LEVEL FEAT ###
		print("##############")
		print("SECOND LEVEL FEAT COMMENCING!!!!")
		print("##############")
		secondlevel_folder = subjfolder + "secondlevel_stop.gfeat"
		feat1 = subjfolder + 'firstlevel_stop_run1.feat'
		feat2 = subjfolder + 'firstlevel_stop_run2.feat'

		if not os.path.exists(feat1) or not os.path.exists(feat2):
				print ("One or more first level feat folders did not complete correctly or does not exist for subject %s. Moving on.%s" %(subject))
				continue

		print ("Second Level Analysis for: %s%s"  %(subject))


		designOutput2 = subjfolder + "secondlevel_stop_design.fsf"
		command = "gsed -e 's|DEFINEOUTPUT|%s|g' -e 's|DEFINEFEAT1|%s|g' -e 's|DEFINEFEAT2|%s|g' %s > %s" %(re.escape(secondlevel_folder),re.escape(feat1), re.escape(feat2),secondleveldesign,designOutput2)
		call(command, shell = True)
		command = "feat %s" %designOutput2
		call(command, shell= True)

		print('i have finished second level feating for %s' %subject)


print("################")
print("ALL DONE! GO TAKE A LOOK @ YOUR DATA!!!!")
print("################")
