//scene 0
function scene_instruction(){
  if (mouseIsPressed) {
    fullscreen(true);
    Time.update();
  } else {
    push();
    fill(col_text);
    textSize(size_text);
    textAlign(CENTER);
    textFont(text_font);
    text( text_start, Pos.center_x, Pos.center_y);
    pop();
  }
}

//scene 1
function scene_fixation(){
  Time.count();
  if (Time.activetime_block < time_fixation) {
    push();
    stroke(col_fixation); // define gray scale color (0 to 255) of lines
    strokeWeight(thick_fixation);
    line(Pos.center_x - len_fixation, Pos.center_y, Pos.center_x + len_fixation, Pos.center_y );
    line(Pos.center_x, Pos.center_y - len_fixation, Pos.center_x, Pos.center_y + len_fixation );
    pop();
  } else {
    Time.update();
  }
}


//scene 2
function scene_targ(){
  if (Time.activetime_block < Params.time_stimduration + time_maskduration){ 
    if (Params.ind_stimcond==Params.ind_previous+1){
      if (flag_practice==true){
        Params.feedback();
      }}
    //  else if(Params.trial_stimcond[Params.ind_stimcond]===3){
    //     let targetIndex=;
    //     Params.saveTrialResults(ind_prev,targetIndex);
    //   }
    
 else{
    Time.update();
  }
}
}

function scene_stim(callback){
  Time.count();

  if (Params.ind_stimcond==Params.ind_previous+1){
    if (keyIsPressed){
      // 32 means space
      if (keyCode == keyRes1) {
        if (Params.flag_gonogo[Params.repetition]==1){
          Time.count_response();
          Params.tmp_res_ob = 1; //1 means the correct response.
        }else{
          Time.count_response();
          Params.tmp_res_ob = 2; //2 means the false alarm.
        }
      }
    }
    else if(!keyIsPressed)
    {
      Time.starttime_nogo();
    }
  }


  if (Time.activetime_block < Params.time_stimduration){    
    push();
    fill(col_target);
    textSize(size_target);
    noStroke();
    textAlign(CENTER);
    textFont(text_font);
    /*code to include the trials with a 3 */
    const currentStimCond = Params.trial_stimcond[Params.ind_stimcond];
    const prevStimCond = Params.trial_stimcond[Params.ind_stimcond - 1];
    
  
     // Check if the previous stimulus condition is not 3 and the current is 3
    if (prevStimCond !== 3 && currentStimCond === 3) {
      // Log the trial information here or perform any other actions you need
      console.log('Logging trial:', prevStimCond, '->', currentStimCond);
      // Params.ind_targ = prevStimCond;
      // Params.ind_previous=null;
    }
    
    
    text(currentStimCond, Pos.center_x, Pos.center_y + size_target / 2);
    pop();
    // text("%d".replace("%d",Params.trial_stimcond[Params.ind_stimcond]), Pos.center_x, (Pos.center_y)+(size_target/2));
    // pop();
  } else{
    callback();
  }
}

// scene 4
function scene_end(){
    push();
    fill(col_text);
    noStroke();
    textSize(size_text);
    textAlign(CENTER);
    text( text_end, Pos.center_x, Pos.center_y);
    pop();
}

function create_end_button(){
  button_end = createButton('END');
  button_end.size(size_end_w,size_end_h);
  button_end.style('font-size', size_end_text + 'px');
  button_end.position(x_end, y_end);
  button_end.mousePressed(quit_task);
  button_end.hide();
}

// this function creates the skip button and it functions similar to the end as it
// skips all the trials and generates the data files.
function create_skip_button(){
  button_skip = createButton('SKIP');
  button_skip.size(size_skip_w, size_skip_h);
  button_skip.position(x_skip, y_skip);
  button_skip.mousePressed(quit_task);
  
}
function show_button_skip(){
 button_skip.show();
}

function quit_task(){
  fullscreen(false);
  /*
  let parameters_to_save = {
    'results_responses': Params.results_responses,
    'results_rt': Params.results_rt,
    'results_ind_previous': Params.results_ind_previous,
    'results_targetvalue': Params.results_targetvalue
  }
post('exit_view_cognitive_task', parameters_to_save, 'post');
*/
  var gogo_data=[];
  var len=Params.blocks.length;
  for(let i=0;i<len;i++)
  {
     let gogotrial_data={
      'Userid' : userid,
      'BlockNo' : Params.blocks[i],
      'Difficulty':Params.diff[i],
      'Start_time':Params.start_time[i],
      'End_time':Params.end_time[i],
      'Results_responses' : Params.results_responses[i],
      'Result_rt' : Params.results_rt[i],
      'Results_ind_previous' :Params.results_ind_previous[i],
      'Results_targetvalue' : Params.results_targetvalue[i]     
    }
    gogo_data.push(gogotrial_data);
    if(Params.results_responses[i]==1)
    {
      Params.score=Params.score+1;
    }
    else if(Params.results_responses[i]==2)
    {
      Params.wrong=Params.wrong+1;
    }
    else{
      Params.notresponded=Params.notresponded+1;
    }
  } 
  alert("Your sore is:- "+ Params.score);
  alert("you have not responded to: "+Params.notresponded+"no of trials")
 const currentDate = new Date();
 const formattedDate = currentDate.toISOString().replace(/:/g, '-').replace(/\./g, '-');

 const fileName = 'gonogo'+`_${formattedDate}`;

 console.log(fileName); 

  //for loacl debugging
  exportCSV(gogo_data,',', fileName);
  location.href='../include/main.html'
  //
}