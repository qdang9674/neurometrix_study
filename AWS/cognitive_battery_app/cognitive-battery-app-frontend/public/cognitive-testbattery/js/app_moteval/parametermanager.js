class ParameterManager{
    constructor() {
      // Stimulus parameters
      this.repetition = 0;
      this.ind_stimcond = 0;
      this.flag_block = false;
      this.flag_load = false;
      this.score=0;
      this.fourcrct=0;
      this.rest=0;
      //save
      this.results_responses = [];
      this.results_rt = [];
      this.results_targetvalue_stim = [];
      this.results_speed_stim = [];
      this.results_correct = [];
      this.blocks=[];
      this.diff=[]; // difficulty array
      this.start_time=[]; // saves start time of the trial
      this.end_time=[]; // saves the end time of the trial
      this.initialize();  
    }
    

      initialize(){
        this.num_rep = num_rep_main;
        this.num_target = num_target_main;
        this.flag_buttoncheck = Array(this.num_totaldot).fill(0);  
        //ConditionManager
        if (count_break==0) {
          this.array_stimcond = array_stimcond_main;
        } else if (count_break==1) {
          this.array_stimcond = array_stimcond_main2;
        } else {
          this.array_stimcond = array_stimcond_main3;
        }
        this.trial_stimcond = shuffle(this.array_stimcond); 
        this.tmp_res_ob = [];
        this.tmp_rt = null;
        this.tmp_st = null;
        this.tmp_et = null;
      }

      next_trial(){
        this.save();
        //set the next trial parameters 
        this.ind_stimcond ++;
        this.flag_load = false;
        this.tmp_res_ob = [];
        this.tmp_rt = null;
        this.tmp_st = null;
        this.tmp_et = null;
        this.flag_buttoncheck = Array(this.num_totaldot).fill(0);
        
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
        this.tmp_res_ob = [];
        this.tmp_rt = null;
        this.tmp_st = null;
        this.tmp_et = null;
        this.flag_buttoncheck = Array(this.num_totaldot).fill(0);
  
        this.flag_block = false;
        this.repetition ++;
        this.trial_stimcond = this.array_stimcond;
        this.ind_stimcond = 0;
        this.num_target = shuffle(this.num_target);
      }
    
      save(){
        // save the current result.
        if(count_break==0)
        {
          block_no=count_break+1;

        }
        else{
          block_no=count_break;
        }
        this.blocks.push(block_no);
        if(block_no==1)
        {
          difficulty=difficulty1;
        } else if(block_no==2)
        {
         difficulty=difficulty2;
         }
        else{
         difficulty=difficulty3;
        }
        this.diff.push(difficulty); // save the difficulty of the current trial.
        this.start_time.push(this.tmp_st); // save the start time of the current trial.
        this.end_time.push(this.tmp_et); // save the end time of the current trial.
        let tmp_ordercheck = 0;;
        for (let i=0;i<this.tmp_res_ob.length;i++){
          if (this.tmp_res_ob[i]>4){
          } else{
            tmp_ordercheck ++;
          }
        }
        this.results_correct.push(tmp_ordercheck/this.tmp_res_ob.length);

        //console.log(this.results_correct)
        //console.log(tmp_ordercheck)
        
        this.results_responses.push(this.tmp_res_ob);
        this.results_rt.push(this.tmp_rt);
        this.results_speed_stim.push(this.trial_stimcond[this.ind_stimcond])
        console.log('response is');
        console.log(this.tmp_res_ob);
      }
  }