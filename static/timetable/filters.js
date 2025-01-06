const checkboxes = document.getElementsByClassName('grades-checkboxes');
const classes = document.getElementsByClassName('class');
const teacher = document.getElementById('teacher-select');
const room = document.getElementById('room-select');


function filterTeachers(){
    console.log(teacher.value);
    if(!(teacher.value === '')){
    for(let i=0; i < classes.length; i++) {

   if (!(classes[i].dataset.teacher.includes(teacher.value))) {
       classes[i].classList.add("teacherFilter");
        } else {
            classes[i].classList.remove('teacherFilter');
        }
    }} else {

        for(let i=0; i < classes.length; i++) {
            classes[i].classList.remove("teacherFilter");
        }
    }
}

function filterRooms(){
    console.log(room.value);
    if(!(room.value === '')){
    for(let i=0; i < classes.length; i++) {

   if (!(classes[i].dataset.room.includes(room.value))) {
       classes[i].classList.add("roomFilter");
        } else {
            classes[i].classList.remove('roomFilter');
        }
    }} else {

        for(let i=0; i < classes.length; i++) {
            classes[i].classList.remove("roomFilter");
        }
    }
}
function filterGrades(){
    let grades = []
    for(let i=0;i<checkboxes.length;i++){
        if(checkboxes[i].checked){
            grades.push(parseInt(checkboxes[i].value));
        }
    }
    if(grades.length > 0){
    for(let i=0;i<classes.length;i++){
        for(let j=0;j<grades.length;j++){
            if(JSON.parse(classes[i].dataset.all_grades).indexOf(grades[j])===-1){
                classes[i].classList.add("filterGrade");
            }
            else {
                classes[i].classList.remove("filterGrade");
                break
            }
        }
    }}
    else {
        for(let i=0;i<classes.length;i++){
            classes[i].classList.remove("filterGrade");
        }
    }
}
function uncheck(){
    teacher.value=""
    room.value=""
    for(const checkbox of checkboxes){
        if(checkbox.checked){
            checkbox.checked=false

        }
    }
    filterTeachers()
    filterGrades()
}