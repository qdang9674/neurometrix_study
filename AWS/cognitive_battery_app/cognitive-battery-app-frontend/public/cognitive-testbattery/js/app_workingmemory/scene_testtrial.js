//scene 0
function scene_instruction(){
  if (mouseIsPressed) {
    fullscreen(true);
    Time.update();
  } else{
    fill(col_text);
    textSize(size_text);
    textAlign(CENTER);
    text( text_start, Pos.center_x, Pos.center_y);
  }
}

//scene 1
function scene_fixation(){
  Time.count();
  if (Time.activetime_block < time_fixation) {
    push();
    stroke(col_fixation); 
    strokeWeight(thick_fixation);
    line(Pos.center_x - len_fixation, Pos.center_y, Pos.center_x + len_fixation, Pos.center_y );
    line(Pos.center_x, Pos.center_y - len_fixation, Pos.center_x, Pos.center_y + len_fixation );
    pop();
  } else{
    Time.update();
  }
}


//scene 2
function scene_targ(){
  Time.count();
  if (Time.activetime_block < time_startblank+(Params.num_memory[Params.ind_stimcond]*time_onestimduration)){
    
    for (let i=0; i < array_stimcond.length; ++i) {
      if (i==Params.count_color && i<Params.num_memory[Params.ind_stimcond]){
        push();
        image(img_obj,Params.dict_pos[Params.trial_stimcond[i]][0],Params.dict_pos[Params.trial_stimcond[i]][1]);
        fill(col_target);
        noStroke();
        rect(Params.dict_pos[Params.trial_stimcond[i]][0],Params.dict_pos[Params.trial_stimcond[i]][1],size_target,size_target);
        pop();
      }else{
        push();
        image(img_obj,Params.dict_pos[Params.trial_stimcond[i]][0],Params.dict_pos[Params.trial_stimcond[i]][1])
        pop();
      }
    }

  } else{
    Time.update();
  }

  if (Time.activetime_block > time_startblank+((Params.count_color+1)*time_onestimduration)){
    Params.count_color ++;
  }
}


function scene_stim(callback){
  if (Params.flag_load == false){   
    //for (let i=0; i < array_stimcond.length; ++i) {
      //Objs[i] = new DrawRect(size_target,Params.dict_pos[Params.trial_stimcond[i]][0],Params.dict_pos[Params.trial_stimcond[i]][1])
    //};
  Time.blockstart();
  Params.flag_load = true;
  } else{
    callback();
  }
}

class DrawRect {
  constructor(size,x,y) {
    noStroke();
    this.size = size;
    this.x = x
    this.y = y
  }

  display() {
    rect(this.x, this.y, this.size, this.size);
  }
 }

// scene 4
function scene_response(){
  Time.count();
  // call function
  for (let i=0; i < array_stimcond.length; ++i) {
    Button[i].mousePressed(record_response);
  
    if (Params.flag_buttoncheck[i] == 1){
      push();
      fill(col_target);
      noStroke();
      rect(Params.dict_pos[Params.trial_stimcond[i]][0],Params.dict_pos[Params.trial_stimcond[i]][1],size_target,size_target);
      pop();
    }
  }


  if (Params.tmp_res_ob.length==Params.num_memory[Params.ind_stimcond]){
    Time.count_response();
    Time.update();
  }
}

function create_answer_button(){
  for (let i=0; i < array_stimcond.length; ++i) {
    Button[i] = createButton("",[i]);
    Button[i].style('font-size', size_text_button + 'px');
    Button[i].size(size_target, size_target);
    Button[i].position(Params.dict_pos[Params.trial_stimcond[i]][0],Params.dict_pos[Params.trial_stimcond[i]][1]);
    Button[i].hide();
  }
}

function show_button(){
  for (let i=0; i < array_stimcond.length; ++i){
    Button[i].show(); 
    Button[i].position(Params.dict_pos[Params.trial_stimcond[i]][0],Params.dict_pos[Params.trial_stimcond[i]][1]);
  }  
}

function switch_buttons_position(){
  var sign = 1;
  if(Button[0].x===Params.dict_pos[Params.trial_stimcond[0]][0]){
    sign = -1;
  }
  for (let i=0; i < array_stimcond.length; ++i) {
    Button[i].position(Params.dict_pos[Params.trial_stimcond[i]][0], Params.dict_pos[Params.trial_stimcond[i]][1] + sign*shift_tuto_y);
  }
}


function record_response(){
  Params.flag_buttoncheck[this.value()] = 1;
  Params.order++;
  Params.tmp_res_ob.push(this.value());
  //console.log(this.value())
}

// scene 5
// function scene_end(){
//   push();
//   fill(col_text);
//   noStroke();
//   textSize(size_text);
//   textAlign(CENTER);
//   text( text_end, Pos.center_x, Pos.center_y);
//   pop();
// }
function scene_end() {
  fullscreen(false);
  push();
  fill(col_text);
  noStroke();
  textSize(size_text);
  textAlign(CENTER);
  text( text_end, Pos.center_x, Pos.center_y);
  pop();

   noLoop(); // Stop the drawing loop if necessary
  // clear(); // Clear the canvas

  // Adjust the END button's position and make it visible
  button_end.position(width / 2 - button_end.size().width / 2, height / 2 + 100); // Adjust Y position as needed
  button_end.show();
}


function create_end_button(){
  button_end = createButton('END');
  button_end.size(size_end_w,size_end_h);
  button_end.style('font-size', size_end_text + 'px');
  button_end.position(x_end, y_end);
  button_end.mousePressed(quit_task);
  button_end.hide();
}

// skip button
// function create_skip_button(){
//   button_skip = createButton('SKIP');
//   button_skip.size(size_skip_w, size_skip_h);
//   button_skip.position(x_skip, y_skip);
//   button_skip.mousePressed(quit_task);
// }
// function show_button_skip(){ 
//  button_skip.show(); // show the skip button
// }

function quit_task(){
  fullscreen(false);
  // button_skip.hide();
  /*
  let parameters_to_save = {
    'results_responses': Params.results_responses,
    'results_targetvalue_stim': Params.results_targetvalue_stim,
    'results_num_stim': Params.results_num_stim
  }
  post('exit_view_cognitive_task', parameters_to_save, 'post');
*/
// var workingmem_data=[];
// var len=Params.blocks.length;
// for(let i=0;i<len;i++)
// {
//   let workingmemtrial_data={
//     'Userid' : userid,
//     'BlockNo': Params.blocks[i],
//     'Difficulty' : Params.diff[i],
//     'Start_time' : Params.start_time[i],
//     'End_time':Params.end_time[i],
//     'Results_responses' :'',
//     'Results_rt' : Params.results_rt[i],
//     'Results_targetvalue_stim' : Params.results_targetvalue_stim[i],
//     'Results_num_stim' : Params.results_num_stim[i],
//     'Results_correct':Params.results_correct[i] 
//   }
//   if (Array.isArray(Params.results_responses[i])) { //loop over the array to join the results into a string 
//     workingmemtrial_data['Results_responses'] = Params.results_responses[i].join("-");
//   } else {
//     workingmemtrial_data['Results_responses'] = Params.results_responses[i];
//   }
//   if(Array.isArray(Params.results_targetvalue_stim[i])){
//     workingmemtrial_data['Results_targetvalue_stim'] = Params.results_targetvalue_stim[i].join("-");
//   }
//   else{
//     workingmemtrial_data['Results_targetvalue_stim'] = Params.results_targetvalue_stim[i];
//   }
//   workingmem_data.push(workingmemtrial_data);
//   // alert(JSON.stringify(workingmemtrial_data));
//   if(Params.results_correct[i]==1)
//   {
//     Params.score=Params.score+1;
//   }
// }

// // alert("Your score is:"+ Params.score);
// const currentDate = new Date();
// const formattedDate = currentDate.toISOString().replace(/:/g, '-').replace(/\./g, '-');
    
// const fileName = `${userid}_`+'workingmemory'+`_${formattedDate}`;
    
// console.log(fileName); 
//     //for loacl debugging
//   exportCSV(workingmem_data,',', fileName);
  location.href='../include/main.html'
  //

}
