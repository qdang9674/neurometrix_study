class ParameterManager{
    constructor() {
      // Stimulus parameters
      this.repetition = 0;
      this.ind_stimcond = 0;
      this.flag_block = false;
      this.flag_load = false;
      this.count_color = -1;
      this.score=0;
      this.flag_buttoncheck = Array(array_stimcond.length).fill(0);

      this.num_rep = num_rep_main;
      if (count_break==0) {
        num_memory_main = num_Array[0];
        console.log(num_memory_main);
      } else if (count_break==1) {
        num_memory_main = num_Array[1];
        console.log(num_memory_main);
      } else {
        num_memory_main = num_Array[2];
        console.log(num_memory_main);
      } 
      //save
      this.results_responses = [];
      this.results_rt = [];
      this.results_targetvalue_stim = [];
      this.results_num_stim = [];
      this.results_correct = [];
      this.blocks=[]; // blocks
      this.diff=[]; // difficulty
      this.start_time=[];// start time 
      this.end_time=[];// end time of the trial
      this.initialize();  
    }

      initialize(){
        //ConditionManager
        this.num_memory = shuffle(num_memory_main);
        let center_x = (Pos.center_x)-(size_target/2);
        let center_y =  (Pos.center_y)-(size_target/2);
        this.dict_pos = [
                          [center_x-1.5*shift_position,center_y-1.5*shift_position],
                          [center_x-0.5*shift_position,center_y-1.5*shift_position],
                          [center_x+0.5*shift_position,center_y-1.5*shift_position],
                          [center_x+1.5*shift_position,center_y-1.5*shift_position],
                          [center_x-1.5*shift_position,center_y-0.5*shift_position],
                          [center_x-0.5*shift_position,center_y-0.5*shift_position],
                          [center_x+0.5*shift_position,center_y-0.5*shift_position],
                          [center_x+1.5*shift_position,center_y-0.5*shift_position],
                          [center_x-1.5*shift_position,center_y+0.5*shift_position],
                          [center_x-0.5*shift_position,center_y+0.5*shift_position],
                          [center_x+0.5*shift_position,center_y+0.5*shift_position],
                          [center_x+1.5*shift_position,center_y+0.5*shift_position],
                          [center_x-1.5*shift_position,center_y+1.5*shift_position],
                          [center_x-0.5*shift_position,center_y+1.5*shift_position],
                          [center_x+0.5*shift_position,center_y+1.5*shift_position],
                          [center_x+1.5*shift_position,center_y+1.5*shift_position],
                        ];
    
        this.trial_stimcond = shuffle(array_stimcond); 
        this.tmp_res_ob = [];
        this.tmp_rt = null;
        this.order = -1;
      }

      next_trial(){
        this.save();

        // send the current trial data to the parent window
        window.parent.postMessage(
          { command: 'working-memory', 
            block_no: this.blocks[this.blocks.length - 1],
            difficulty: this.diff[this.diff.length - 1],
            start_time: this.start_time[this.start_time.length - 1],
            end_time: this.end_time[this.end_time.length - 1],
            results_responses: this.results_responses[this.results_responses.length - 1],
            results_rt: this.results_rt[this.results_rt.length - 1],
            results_targetvalue_stim: this.results_targetvalue_stim[this.results_targetvalue_stim.length - 1],
            results_num_stim: this.results_num_stim[this.results_num_stim.length - 1],
            results_correct: this.results_correct[this.results_correct.length - 1]
          }, 
        '*');

        //set the next trial parameters 
        this.ind_stimcond ++;
        this.flag_load = false;
        this.tmp_res_ob = [];
        this.tmp_rt = null;
        this.count_color = -1;
        this.order = -1;
        this.flag_buttoncheck = Array(array_stimcond.length).fill(0);
        this.trial_stimcond = shuffle(array_stimcond);
  
        if (this.ind_stimcond==this.num_memory.length-1){
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
        this.tmp_res_ob = [];
        this.tmp_rt = null;
        this.count_color = -1;
        this.order = -1;
        this.flag_buttoncheck = Array(array_stimcond.length).fill(0);
  
  
        this.flag_block = false;
        this.repetition ++;
        this.trial_stimcond = shuffle(array_stimcond); 
        this.ind_stimcond = 0;
        //this.num_memory = shuffle(this.num_memory);
      }
    
      save(){
        if(count_break==0)
        {
          block_no=count_break+1;
        }
        else{
          block_no=count_break;
        }
        this.blocks.push(block_no);
        if(num_memory_main==num_memory_main3)
        {
          difficulty=difficulty3;
        }
        else if(num_memory_main==num_memory_main2)
        {
          difficulty=difficulty2;
        }
        else{
          difficulty=difficulty1;
        }
        this.diff.push(difficulty); // saves the difficulty of the current trial
        this.start_time.push(this.tmp_st); // saves the starttime of the current trial
        this.end_time.push(this.tmp_et);// saves the end time of the currrent trial
        // save the current result.
        let tmp_ordercheck =0
        for (let i=0;i<this.tmp_res_ob.length;i++){
        tmp_ordercheck = tmp_ordercheck+Math.abs(this.tmp_res_ob[i]-i);
        }
        if (tmp_ordercheck==0){
          this.results_correct.push(1);
        } else{
          this.results_correct.push(0);
        }
        //console.log(this.results_correct)
        //console.log(tmp_ordercheck)
        
        this.results_responses.push(this.tmp_res_ob);
        this.results_rt.push(this.tmp_rt);
        this.results_targetvalue_stim.push(this.trial_stimcond);
        this.results_num_stim.push(this.num_memory[this.ind_stimcond])
        //console.log('response is');
        //console.log(this.tmp_res_ob);
      }
  }
  