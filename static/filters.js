const checkboxes = document.getElementsByClassName('grades-checkboxes');
const classes = document.getElementsByClassName('class');
const teacher = document.getElementById('teacher-select');


function filterTeachers(){
    for(let i=0; i < classes.length; i++){

        if(!(classes[i].dataset.teacher === teacher.value)){
            classes[i].hidden = true;
            console.log("true")
        }
        else {
            classes[i].hidden = false;
        }
    }
}
function filterGrades(){
    let grades = []
    for(let i=0;i<checkboxes.length;i++){
        if(checkboxes[i].checked){
            grades.push(checkboxes[i].value);
        }
    }
    if(grades.length > 0){
    console.log(grades)
    for(let i=0;i<classes.length;i++){
        for(let j=0;j<grades.length;j++){
            console.log(classes[i].dataset.all_grades.includes(grades[j]));
            if(!(classes[i].dataset.all_grades.includes(grades[j]))){
                classes[i].hidden = true;
            }
            else {
                classes[i].hidden = false;
            }
        }
    }}
    else {
        for(let i=0;i<classes.length;i++){
            classes[i].hidden =false
        }
    }
}