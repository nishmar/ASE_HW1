#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 13:10:00 2017

@author: nishi
"""
import re
import glob
import string


#Check how many speaker per file
def speakers():
    
    transcript_path= '/Users/nishi/Google Drive/OldMacFolders/Research_Topics/final_bangor/transcripts_clean5/'
    file_list= glob.glob("%s*.cha" % transcript_path)
    outf = open('transcripts_3+_speakers', 'w')
    outf.write('#Note: OS* == Non-participant\n\n')
    
    for fl in file_list:
        f = open(fl, 'r')
        all_lines = f.readlines()
        f.close()
        
        speaker_count=0
        speaker_list=[]
        
        for line in all_lines:
            if line[0]=='@':
                if re.search(r'ID', line)!=None:
                    speaker_list.append(line)
                    speaker_count+=1
               
        if speaker_count > 2:
            outf.write(fl[len(transcript_path):] + '\n')
            for speaker in speaker_list:
                outf.write(speaker)
            
            outf.write('\n')
    outf.close()     

#Sort the crowdsourced bangor corpus 
def sort(fl, bangor_path):
    # Open .conll file
    
    f = open(fl, 'r')
    
    out_folder= '/Users/nishi/GitHubReps/crowdsourced_bangor_sorted/'
        
    """
    Sort function
    """
    
    sent_ids = []
    speaker_turns=[]
    all_lines = f.readlines()
    f.close()
    
    for i in range (0,len(all_lines)):
        if all_lines[i][0] == '#':
            sent_ids.append(all_lines[i])
            tokens = []
            j=i+1
            while all_lines[j][0]!='\n':
                tokens.append(all_lines[j])
                j+=1
            speaker_turns.append(tokens)      
    
    
    id_set=[]
         
    for sid in sent_ids:    
        full_id = sid[re.search(r"\d",sid).start():]
        #print full_id
        
        [start_id, end_id] = re.split(r"_",full_id,1)
        start_id = string.replace(start_id, '\x15', '')
        id_set.append(int(start_id))
        #print end_id

    id_set_zip = zip(id_set,sent_ids, speaker_turns)
    
    sorted_ids = sorted(id_set_zip)
    
    outf = open(out_folder+fl[len(bangor_path):], 'w')
    
    for start_time, sent_id, turn in sorted_ids:
        outf.write(sent_id)
        for token in turn:
            outf.write(token)
        outf.write('\n')
           
"""
"""            
bangor_path = '/Users/nishi/GitHubReps/crowdsourced_bangor/'

#speakers() 

file_list= glob.glob("%s*.cha.conll" % bangor_path)

for fl in file_list: 
    sort(fl, bangor_path)

