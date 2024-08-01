const checkboxes = document.getElementsByClassName('grades-checkboxes');
const classes = document.getElementsByClassName('class');
const teacher = document.getElementById('teacher-select');


function filterTeachers(){
    console.log(teacher.value);
    if(!(teacher.value === '')){
    for(let i=0; i < classes.length; i++) {

        if (!(classes[i].dataset.teacher === teacher.value)) {
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
function filterGrades(){
    let grades = []
    for(let i=0;i<checkboxes.length;i++){
        if(checkboxes[i].checked){
            grades.push(parseInt(checkboxes[i].value));
        }
    }
    if(grades.length > 0){
    console.log(grades)
    for(let i=0;i<classes.length;i++){
        console.log("run")
        for(let j=0;j<grades.length;j++){
            console.log(classes[i].dataset.all_grades);
            console.log(JSON.parse(classes[i].dataset.all_grades));
            if(JSON.parse(classes[i].dataset.all_grades).indexOf(grades[j])){
                classes[i].classList.add("filterGrade");
            }
            else {
                classes[i].classList.remove("filterGrade");
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
    for(const checkbox of checkboxes){
        if(checkbox.checked){
            checkbox.checked=false

        }
    }
    filterGrades()
}