#This program will make EV files from the logfile collected during StopSignal Task in fmri

#Sarah Hennessy, 2018


import os
import sys
import csv
import pandas as pd
import numpy as np

#reload(sys)



datafolder = "/Volumes/MusicProject/School_Study/Data/Functional/Logfiles/Gr5/Baseline/stop"
#subjectlist = [elem for elem in os.listdir(datafolder) if "run" in elem]

subjectlist = [elem for elem in os.listdir(datafolder) if "5" in elem]


print ('your subject list is:',subjectlist)

subject_outpath = "/Volumes/MusicProject/School_Study/Data/Functional/Gr5/Baseline/Music"




for subject in subjectlist: #subject = indiv file
    subj = subject
    subjectfolder = datafolder + "/%s" %(subject)
    evfolder = subject_outpath + '/%sbaseline' %(subj)
    if os.path.exists(evfolder):
        evlist = [elem for elem in os.listdir(subjectfolder) if "run" in elem]
        #subj = subject

        for log in evlist:
            run = log[-5]
            print("you are working on %s, run: %s" %(subj, run))
            #print(log)

            #log = datafolder + '/%s_stop_run%s.txt' %(subj, run)

            log_path_full = subjectfolder + "/%s" %(log)
            #print(log_path_full)


            #evpath = "/Volumes/MusicProject/AllMatlabScripts/fMRI/stop/EV"




            data = pd.read_csv(log_path_full, delim_whitespace = True, comment = "#", header = "infer", skip_blank_lines = True, engine = "python")

            maxlen = data.shape[0]

            for index, row in data.iterrows():



        #CORRECTGO

                if row.condition == 'go' and row.accuracy == 1:
                    revfilename = evfolder + '/go_correct_resp_run%s.txt' %(run)
                    revfile = open(revfilename, 'a')
                    revfile.write('%0.4f\t%0.4f\t1\n' %(row.stimonset, row.stimlength))
                    revfile.close()



            #INCORRECT GO

                elif row.condition == 'go' and row.accuracy == 0:
                    revfilename = evfolder + '/go_incorrect_resp_run%s.txt' %(run)
                    revfile = open(revfilename, 'a')
                    revfile.write('%0.4f\t%0.4f\t1\n' %(row.stimonset, row.stimlength))
                    revfile.close()


            #CORRECT STOP
                elif row.condition == 'stopsignal' and row.accuracy == 1:
                    revfilename = evfolder + '/stop_correct_resp_run%s.txt' %(run)
                    revfile = open(revfilename, 'a')
                    revfile.write('%0.4f\t%0.4f\t1\n' %(row.stimonset, row.stimlength))
                    revfile.close()



            #INCORRECT STOP
                elif row.condition == 'stopsignal' and row.accuracy == 0:
                    revfilename = evfolder + '/stop_incorrect_resp_run%s.txt' %(run)
                    revfile = open(revfilename, 'a')
                    revfile.write('%0.4f\t%0.4f\t1\n' %(row.stimonset, row.stimlength))
                    revfile.close()
