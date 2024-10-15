class ParameterManager{
    constructor() {
      // Stimulus parameters
      this.repetition = 0;
      this.ind_stimcond = 0;
      this.flag_block = false;

      this.num_rep =num_rep_main;
      this.score=0;
      this.notresponded=0;
  
      // Results parameters;
      this.tmp_res_ob = 0;
      this.tmp_rt = null;
      this.tmp_st = null;
      this.tmp_et = null;
      this.results_responses = [];
      this.results_rt = [];
      this.results_ind_switch = [];
      this.results_indtask = [];
      this.results_trial_target = [];
      this.blockno=[];
      this.diff=[];
      this.startt=[];
      this.endt=[];
      this.initialize();
      

    } 

    initialize(){
      // condition setting
      this.ind_switch = [];      
      this.trial_target = shuffle(array_target);
      for (let i=0;i<this.num_rep;i++){
        this.ind_switch = concat(this.ind_switch,array_stimcond);
      }
      this.ind_switch = shuffle(this.ind_switch);
  
      this.ind_task = shuffle(array_taskcond); 
      this.ind_task = int(this.ind_task[0]); //initialize the first task;
      if (count_break==0) {
        // time_stimduration = time_stimduration;
        time_stimduration = timeDurations[0]; // assign the randomized black number 
        // console.log(time_stimduration);
      } else if (count_break==1) {
        // time_stimduration = time_stimduration2;
        time_stimduration = timeDurations[1];
        // console.log(time_stimduration);
      } else {
        // time_stimduration = time_stimduration3;
        time_stimduration = timeDurations[2];
        // console.log(time_stimduration);
      }
    }
    
    next_trial(){
      this.save(); //This task saves the data once per block.

      // send the current trial data to the parent window
      window.parent.postMessage(
        { command: 'task-switching', 
          block_no: this.blockno[this.blockno.length - 1],
          difficulty: this.diff[this.diff.length - 1],
          start_time: this.startt[this.startt.length - 1],
          end_time: this.endt[this.endt.length - 1],
          results_responses: this.results_responses[this.results_responses.length - 1],
          results_rt: this.results_rt[this.results_rt.length - 1],
          results_ind_switch: this.results_ind_switch[this.results_ind_switch.length - 1],
          results_indtask: this.results_indtask[this.results_indtask.length - 1],
          results_trail_target: this.results_trial_target[this.results_trial_target.length - 1]
        }, 
      '*');
  
      //set the next trial parameters
      this.set_stimlusorder_trial();
      this.ind_stimcond ++;
      this.tmp_res_ob = 0;
      this.tmp_rt = null;
      this.tmp_st = null;
      this.tmp_et = null;
      if (this.ind_stimcond==this.ind_switch.length){
        this.flag_block = true;
        if (count_break==0 & flag_practice==false) {
          count_break ++;
        }
      }
    }
  
    next_block(){
      //in this experiment, this function is just for the save of the last trial.
      //The last value of the ind_switch is the same as the one before just for pudding.
      this.ind_stimcond = this.ind_stimcond-1;
      this.save(); 
    }
  
    set_stimlusorder_trial(){
      if (this.ind_switch[this.ind_stimcond]==1){
        this.ind_task = Math.abs(this.ind_task -1);
      }
      this.trial_target = shuffle(array_target);
    }
  
  
    save(){
      // store the current stimulus and response data to the result dictionary.
      if(count_break==0){
        block_number=count_break+1;
      }
      else{
        block_number=count_break;
      }
      this.blockno.push(block_number);
      // if(block_no==1)
      // {
      //   difficulty=difficulty1;
      // }
      // else if(block_no==2)
      // {
      //   difficulty=difficulty2;
      // }
      // else{
      //   difficulty=difficulty3;
      // }
      // Randomization of the blocks 
      if(time_stimduration==time_comp_temp)
      {
        difficulty=difficulty1;
      } else if(time_stimduration==time_stimduration2)
      {
        difficulty=difficulty2;
      }
      else{
        difficulty=difficulty3;
      }
      this.diff.push(difficulty);
      this.startt.push(this.tmp_st);
      this.endt.push(this.tmp_et);
      this.results_responses.push(this.tmp_res_ob);
      this.results_rt.push(this.tmp_rt);
      this.results_ind_switch.push(this.ind_switch[this.ind_stimcond]);
      this.results_indtask.push(this.ind_task);
      this.results_trial_target.push(this.trial_target[0]);
    }
  }
  
  