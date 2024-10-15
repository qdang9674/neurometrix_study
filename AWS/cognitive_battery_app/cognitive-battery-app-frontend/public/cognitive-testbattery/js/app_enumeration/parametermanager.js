class ParameterManager{
    constructor() {
      // Stimulus parameters
      this.repetition = 0;
      this.ind_stimcond = 0;
      this.flag_block = false;

      this.num_rep = num_rep_main;
      this.time_stimduration = time_stimduration_main;
      this.array_stimcond = array_stimcond_main;
      this.trial_stimcond = shuffle(this.array_stimcond);
      this.flag_load = false;
      this.score=0;

      // this.timeDurations = [time_stimduration_main, time_stimduration_main2, time_stimduration_main3];
      // this.shuffleArray(this.timeDurations);  
      for(let i=0;i<timeDurations.length;i++) 
      {
        console.log(timeDurations[i]);
      }

      //ConditionManager
      if (count_break==0) {
        time_stimduration_main = timeDurations[0];// assign the randomized blocks
         console.log(time_stimduration_main);
      } else if (count_break==1) {
        time_stimduration_main = timeDurations[1];
        console.log(time_stimduration_main);
        
      } else {
        time_stimduration_main = timeDurations[2];
        console.log(time_stimduration_main);
      }

  
      this.tmp_res_ob = 0;
      this.tmp_rt = null;
      this.tmp_st = null;
      this.tmp_et=null;
      this.results_responses = [];
      this.results_rt = [];
      this.results_targetvalue = [];
      this.blocks=[]; // block numbers
      this.diff=[]; // difficulty 
      this.start_time=[]; // Time stamps Start time 
      this.end_time=[];// Time stamp End time
      
     

    }

    next_trial(){
      this.save(); 

      // send current trial data to the parent window
      window.parent.postMessage(
        { command: 'enumeration', 
          block_no: this.blocks[this.blocks.length - 1],
          difficulty: this.diff[this.diff.length - 1],
          start_time: this.start_time[this.start_time.length - 1],
          end_time: this.end_time[this.end_time.length - 1],
          results_responses: this.results_responses[this.results_responses.length - 1],
          results_rt: this.results_rt[this.results_rt.length - 1],
          results_targetvalue: this.results_targetvalue[this.results_targetvalue.length - 1]
        }, 
      '*');

      //set the next trial parameters
      this.flag_load = false;
      this.ind_stimcond ++;
      this.tmp_res_ob = 0;
      this.tmp_rt = null;
      this.tmp_st=null;
      this.tmp_et=null;
      if (this.ind_stimcond==this.array_stimcond.length-1){
        this.flag_block = true;
        if (count_break==0 & flag_practice==false) {
          count_break ++;
   
        }
      }
    }
  
    next_block(){
      this.save(); 

      //set the next block parameters
      this.flag_load = false;
      this.repetition ++;
      this.trial_stimcond = shuffle(this.array_stimcond);
      this.ind_stimcond = 0;
      this.flag_block = false;
      this.tmp_res_ob = 0;
      this.tmp_rt = null;
      this.tmp_st=null;
      this.tmp_et=null;
    }
   
    save(){
      // save the current result.
      if(count_break==0){
        block_no=count_break+1;
      }
      else{
        block_no=count_break;
      }
      this.blocks.push(block_no);
      if(time_stimduration_main==500)
      {
        difficulty=difficulty1;
      } else if(time_stimduration_main==250)
      {
        difficulty=difficulty2;
      }
      else{
        difficulty=difficulty3;
      }
      this.diff.push(difficulty); // save the current difficulty 
      this.start_time.push(this.tmp_st); // save the current start time of the trial
      this.end_time.push(this.tmp_et); // save the current end time of the trial 
      this.results_responses.push(this.tmp_res_ob);
      this.results_rt.push(this.tmp_rt);
      this.results_targetvalue.push(this.trial_stimcond[this.ind_stimcond]);

    
    }
  
  }
  