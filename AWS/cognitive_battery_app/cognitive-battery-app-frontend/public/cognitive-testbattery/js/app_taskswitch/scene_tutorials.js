
// scene 6
function scene_tutorial1(){
    draw_character(researcher_2,pos_researcher_x,pos_researcher_y,researcher_width, researcher_width);
    draw_background_bubble(Pos.center_x, pos_bubble_y,size_bubble_x,size_bubble_y);
    //Title
    push();
    fill(col_titletext);
    textSize(size_titletext);
    textAlign(CENTER);
    textFont(text_font);
    text( text_title_0, pos_title_x, pos_title_y);
    pop();

    push();
    fill(col_tutorialtext);
    textSize(size_tutorialtext);
    textAlign(CENTER);
    textFont(text_font);
    text( text_tutorial_0_0, pos_tutorialtext_x, pos_tutorialtext_y-2*shift_text);
    text( text_tutorial_0_1, pos_tutorialtext_x, pos_tutorialtext_y-shift_text);
    text( text_tutorial_0_2, pos_tutorialtext_x, pos_tutorialtext_y);
    text( text_tutorial_0_3, pos_tutorialtext_x, pos_tutorialtext_y+shift_text);
    pop();

    //button
    button_next.mousePressed(()=>{
        button_previous.show();
        Time.update_tutorial_next();    
        });
}

function create_next_button(){
    button_next = createButton('Next');
    button_next.size(size_next_w,size_next_h);
    button_next.style('font-size', size_next_text + 'px');
    button_next.position(x_next, y_next);
    button_next.hide();
}

function create_previous_button(){
    button_previous = createButton('Previous');
    button_previous.size(size_previous_w,size_previous_h);
    button_previous.style('font-size', size_previous_text + 'px');
    button_previous.position(x_previous, y_previous);
    button_previous.hide();
}


// scene 7
function scene_tutorial2(){
    draw_character(researcher_3,pos_researcher_x,pos_researcher_y,researcher_width, researcher_width);
    draw_background_bubble(Pos.center_x-3*shift_text, pos_bubble_y+3*shift_text,size_bubble_x,size_bubble_y);
    //image
    demo_img0();
    //text
    push();
    fill(col_tutorialtext);
    textSize(size_tutorialtext);
    textAlign(CENTER);
    textFont(text_font);
    text( text_tutorial_1_0, pos_tutorialtext_x1, pos_tutorialtext_y1+shift_text);
    text( text_tutorial_1_1, pos_tutorialtext_x1, pos_tutorialtext_y1+2*shift_text);
    text( text_tutorial_1_2, pos_tutorialtext_x1, pos_tutorialtext_y1+3*shift_text);
    pop();
    //buttons
    button_next.mousePressed(()=>{
        Time.update_tutorial_next();    
        });
    button_previous.mousePressed(()=>{
        button_previous.hide();
        Time.update_tutorial_previous();    
        });
}

function demo_img0(){
    push();
    fill(col_instruction);
    textSize(size_instruct_txt);
    noStroke();
    textAlign(CENTER);
    textFont(text_font);
    image(img_task1,Pos.center_x-(size_obj/2), pos_image_y1);
    image(img_instruct1,x_instruct, pos_image_2_y1);
    text(text_1left,x_instruct_text1,y_instruct_text_tuto);
    text(text_1right,x_instruct_text2,y_instruct_text_tuto);
    pop();
    push();
    fill(col_instruction);
    textSize(size_instruction);
    noStroke();
    textAlign(CENTER);
    textFont(text_font);
    text("8", Pos.center_x, pos_image_y1+(size_obj/2)+(size_instruction/2));
    pop();

}



// scene 8
function scene_tutorial3(){
    //image
    demo_img1();
    draw_character(researcher_2,pos_researcher_x,pos_researcher_y,researcher_width, researcher_width);
    draw_background_bubble(Pos.center_x-3*shift_text, pos_bubble_y+3*shift_text,size_bubble_x,size_bubble_y);
    //text
    push();
    fill(col_tutorialtext);
    textSize(size_tutorialtext);
    textAlign(CENTER);
    textFont(text_font);
    text( text_tutorial_2_0, pos_tutorialtext_x1, pos_tutorialtext_y2+shift_text);
    text( text_tutorial_2_1, pos_tutorialtext_x1, pos_tutorialtext_y2+2*shift_text);
    text( text_tutorial_2_2, pos_tutorialtext_x1, pos_tutorialtext_y2+3*shift_text);
    pop();
    //buttons
    button_next.mousePressed(()=>{
        button_next.hide();
        button_start.show();
        Time.update_tutorial_next();    
        });
    button_previous.mousePressed(()=>{
        Time.update_tutorial_previous();    
        });
}

function demo_img1(){
    push();
    fill(col_instruction);
    textSize(size_instruct_txt);
    noStroke();
    textAlign(CENTER);
    textFont(text_font);
    image(img_task2,Pos.center_x-(size_obj/2), pos_image_y1);
    image(img_instruct2,x_instruct, pos_image_2_y1);
    text(text_2left,x_instruct_text1,y_instruct_text_tuto);
    text(text_2right,x_instruct_text2,y_instruct_text_tuto);
    pop();
    push();
    fill(col_instruction);
    textSize(size_instruction);
    noStroke();
    textAlign(CENTER);
    textFont(text_font);
    text("8", Pos.center_x, pos_image_y1+(size_obj/2)+(size_instruction/2));
    pop();
}

// scene 9
function scene_tutorial4(){
    draw_character(researcher_3, pos_researcher_x,pos_researcher_y, researcher_width, researcher_width);


    //text
    push();
    fill(col_tutorialtext);
    textSize(size_tutorialtext3);
    textAlign(CENTER);
    textFont(text_font);
    text(text_tutorial_3_0, pos_tutorialtext_x3, pos_tutorialtext_y3);
    pop();

    //buttons
    button_previous.mousePressed(()=>{
        button_next.show();
        button_start.hide();
        Time.update_tutorial_previous();    
        });
    button_start.mousePressed(()=>{
        button_previous.hide();
        button_start.hide();
        Params.num_rep = num_rep_practice;
        Params.initialize();
        Time.start();    
        });    
}

function create_start_button(){
    button_start = createButton('Start');
    button_start.size(size_start_w,size_start_h);
    button_start.style('font-size', size_start_text + 'px');
    button_start.position(x_start, y_start);
    button_start.hide();
}

function scene_tutorial5(){
    draw_character(researcher_3, pos_researcher_x,pos_researcher_y, researcher_width, researcher_width);

    //text
    push();
    fill(col_tutorialtext);
    textSize(size_tutorialtext3);
    textAlign(CENTER);
    text(text_tutorial_4_0, pos_tutorialtext_x3, pos_tutorialtext_y3);
    pop();

    //buttons
    button_start.mousePressed(()=>{
        button_start.hide();
        Params = new ParameterManager();
        Params.num_rep = num_rep_main;
        flag_practice = false;
        flag_break = true;
        Time.start();    
        });    
}

let linkRect; 
let count=0;
function scene_break() {
    fullscreen(false);
    draw_character(researcher_2, pos_researcher_x, pos_researcher_y, researcher_width, researcher_width);
    draw_background_bubble(Pos.center_x, pos_bubble_y2, size_bubble_x, size_bubble_y);
    button_start.hide();
    // Title "Break time."
    push();
    fill(col_tutorialtext);
    textSize(size_tutorialtext3);
    textAlign(CENTER);
    text(text_tutorial_5_0, pos_tutorialtext_x3, pos_tutorialtext_y3);
    pop();

    // Adjust the y-coordinate for each subsequent piece of text and the link
    let currentY = pos_tutorialtext_y3 + 60; // Increment this to move the next element down

    // Text for "Thank you for your effort. When you are ready,"
    push();
    fill(col_tutorialtext);
    textSize(size_tutorialtext);
    textAlign(CENTER);
    textFont(text_font);
    text(text_tutorial_6_1, pos_tutorialtext_x, currentY);
    pop();

    // Increment currentY for the last piece of text before the button
    currentY += 40;

    // Text for "please click the start button to restart."
    push();
    fill(col_tutorialtext);
    textSize(size_tutorialtext);
    textAlign(CENTER);
    textFont(text_font);
    text(text_tutorial_6_2, pos_tutorialtext_x, currentY);
    pop();

    // Increment currentY for the button
    currentY += 60;
    button_start.position(x_start, currentY);
    button_start.show();

    //buttons
    button_start.mousePressed(()=>{
        button_start.hide();
        count=0;
        fullscreen(true);
        // mouseClicked();
        tmp_save();
        Params = new ParameterManager();
        tmp_connect();
        Params.num_rep = num_rep_main;
        flag_practice = false;
        count_break ++;
        if (count_break==max_break-1){
            flag_break = false;
        }else{
            flag_break = true;
        }
        Time.start();    
        });   
}
// function mouseClicked() {
//     if (
//         mouseX >= linkRect.x &&
//         mouseX <= linkRect.x + linkRect.width &&
//         mouseY >= linkRect.y &&
//         mouseY <= linkRect.y + linkRect.height
//     ) {
//         window.open(linkRect.url, '_blank');
//         linkRect = null; // Remove the link rectangle
//     }

    
// }

let tmp1 = [];
let tmp2 = [];
let tmp3 = [];
let tmp4 = [];
let tmp5 = [];
let tmp6 = [];
let tmp7 = [];
let tmp8 = [];
let tmp9 = [];

function tmp_save(){
    tmp1 = Params.blockno;
    tmp2 = Params.diff;
    tmp3 = Params.startt;
    tmp4 = Params.endt;
    tmp5 = Params.results_responses;
    tmp6 = Params.results_rt;
    tmp7 = Params.results_ind_switch;
    tmp8 = Params.results_indtask;
    tmp9 = Params.results_trial_target;

}
function tmp_connect(){
    for(let i=0;i<tmp1.length;i++){
    Params.blockno.push(tmp1[i]);
    }
    for(let i=0;i<tmp2.length;i++){
        Params.diff.push(tmp2[i]);  
    }
    for(let i=0;i<tmp3.length;i++){
        Params.startt.push(tmp3[i]); 
    }
    for(let i=0;i<tmp4.length;i++){
        Params.endt.push(tmp4[i]); 
    }
    for(let i=0;i<tmp5.length;i++){
        Params.results_responses.push(tmp5[i]);
    }
    for(let i=0;i<tmp6.length;i++){
        Params.results_rt.push(tmp6[i]);
    }
    for(let i=0;i<tmp7.length;i++){
        Params.results_ind_switch.push(tmp7[i]);
    }
    for(let i=0;i<tmp8.length;i++){
        Params.results_indtask.push(tmp8[i]);
    }
    for(let i=0;i<tmp9.length;i++){
        Params.results_trial_target.push(tmp9[i]);
    }
    
    
    
    
}
