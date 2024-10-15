//scene 0
function scene_instruction(){
  if (mouseIsPressed) {
    fullscreen(true);
    Time.update();
  } else {
    fill(col_text);
    textSize(size_text);
    textAlign(CENTER);
    text( text_start, Pos.center_x, (Pos.center_y)+(size_text/2));
  }
}

//scene 1

function scene_fixation(){
  Time.count();
  if (Time.activetime_block < time_fixation) {
    push();
    fill(col_instruction);
    textSize(size_instruct_txt);
    noStroke();
    textAlign(CENTER);
    if (Params.ind_task ==0){
      image(img_task1,Pos.center_x-(size_obj/2), Pos.center_y-(size_obj/2));
      image(img_instruct1,x_instruct, y_instruct);
      text(text_1left,x_instruct_text1,y_instruct_text);
      text(text_1right,x_instruct_text2,y_instruct_text);
    }else{
      image(img_task2,Pos.center_x-(size_obj/2), Pos.center_y-(size_obj/2));
      image(img_instruct2,x_instruct, y_instruct);
      text(text_2left,x_instruct_text1,y_instruct_text);
      text(text_2right,x_instruct_text2,y_instruct_text);
    }
    pop();

  } else {
    Time.update();
  }
}



//scene 2
function scene_stim(){
  Time.count();
  if (keyIsPressed){
    if (keyCode == keyRes1) {
      Time.count_response();
      Params.tmp_res_ob = 1;
      Time.update();
    } else if (keyCode == keyRes2) {
      Time.count_response();
      Params.tmp_res_ob = 2;
      Time.update();
    }
    
  }
  else if(!keyIsPressed){
    Time.starttime_nores();
  }

  if (Time.activetime_block < time_stimduration){    
    push();
    fill(col_instruction);
    textSize(size_instruct_txt);
    noStroke();
    textAlign(CENTER);
    if (Params.ind_task ==0){
      image(img_task1,Pos.center_x-(size_obj/2), Pos.center_y-(size_obj/2));
      image(img_instruct1,x_instruct, y_instruct);
      text(text_1left,x_instruct_text1,y_instruct_text);
      text(text_1right,x_instruct_text2,y_instruct_text);
    }else{
      image(img_task2,Pos.center_x-(size_obj/2), Pos.center_y-(size_obj/2));
      image(img_instruct2,x_instruct, y_instruct);
      text(text_2left,x_instruct_text1,y_instruct_text);
      text(text_2right,x_instruct_text2,y_instruct_text);
    }
    pop();
    push();
    fill(col_instruction);
    textSize(size_instruction);
    noStroke();
    textAlign(CENTER);
    text("%d".replace("%d",Params.trial_target[0]), Pos.center_x, (Pos.center_y)+(size_instruction/2));    
    pop();
    
  } else{
    Time.update();
  }
}




function scene_backmask(){
  Time.count();
  if (Time.activetime_block <  time_maskduration){
    //show a blank for this experiment
    //image(img, (Pos.center_x)-(size_img[0]/2), (Pos.center_y)-(size_img[1]/2));
  } else{
    Time.update();
  }
}

// scene 3
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
  console.log("scene_end called");
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

// function create_skip_button(){
//   button_skip = createButton('SKIP');
//   button_skip.size(size_skip_w, size_skip_h);
//   button_skip.position(x_skip, y_skip);
//   button_skip.mousePressed(quit_task);
  
//   //button_skip.onPress = function() {
//   //   time_manager.scene = time_manager.end_scene;
//  //};

// }
// function show_button_skip(){
//  button_skip.show();
// }

function quit_task(){
  fullscreen(false);
  /*
  let parameters_to_save = {
    'results_responses': Params.results_responses,
    'results_rt': Params.results_rt,
    'results_ind_switch': Params.results_ind_switch,
    'results_indtask': Params.results_indtask
  }
  post('exit_view_cognitive_task', parameters_to_save, 'post');
*/
 
// var data= [];
// var len=Params.blockno.length;


// for(let i=0;i<len;i++)
// {
//   let trial_data= {
//     'Userid': userid,
//     'Blockno': Params.blockno[i],
//     'Difficulty': Params.diff[i],
//     'Start_time': Params.startt[i],
//     'End_time': Params.endt[i],
//     'Results_Responses': Params.results_responses[i],
//     'Results_rt': Params.results_rt[i],
//     'Results_ind_switch': Params.results_ind_switch[i],
//     'Results_indtask': Params.results_indtask[i],
//     'Results_trail_target': Params.results_trial_target[i]
//   };

//   data.push(trial_data);
//   if(Params.results_indtask[i]==1)
//   { 
//     if(Params.results_trial_target[i]>5 && Params.results_responses[i]==2)
//     {
//       Params.score=Params.score+1;
//     }
//     else if(Params.results_trial_target[i]<5 && Params.results_responses[i]==1)
//     {
//       Params.score=Params.score+1;
//     }
//     else if(Params.results_responses[i]==0){
//       Params.notresponded=Params.notresponded+1;
//     }

//   }
//   else if(Params.results_indtask[i]==0)
//   {
//     if(Params.results_trial_target[i]%2==0 && Params.results_responses[i]==2)
//     {
//       Params.score=Params.score+1;
//     }
//     else if(Params.results_trial_target[i]%2!=0 && Params.results_responses[i]==1)
//     {
//       Params.score=Params.score+1;
//     }
//     else if(Params.results_responses[i]==0){
//       Params.notresponded=Params.notresponded+1;
//     }
//   }
 
// } 

// const currentDate = new Date();
// const formattedDate = currentDate.toISOString().replace(/:/g, '-').replace(/\./g, '-');
    
// const fileName = `${userid}_`+'taskswitching'+`_${formattedDate}`;
    
// // console.log(fileName);

// // alert("Your score is : "+Params.score+"You have not responded to "+Params.notresponded+" No of trials");
 
//     //for loacl debugging
//   exportCSV(data,',', fileName);
    
    location.href='../include/main.html'

    //

}
  