// Return an array of the selected option values in the control.
// Select is an HTML select element.
function getSelectValues(select) {
  var result = [];
  var options = select && select.options;
  var opt;
  for (var i=0, iLen=options.length; i<iLen; i++) {
    opt = options[i];
    if (opt.selected) {
      result.push(opt.value || opt.text);
    }
  }
  return result;
}
const classesByHour = JSON.parse(document.getElementById("ClassesByHour").textContent)
        function markClasses(){
        Object.keys(classesByHour).forEach(function(key) {
           let button = document.getElementById(key)
            button.style.background = `rgba(195, 201, 83,${classesByHour[key]/14.5})`;
            button.innerText = classesByHour[key]
        });
        }
    function resetBoard(reset){
        const hour = document.getElementById("hour")
        const day = document.getElementById("day")
        const buttons = document.getElementsByClassName("timeframe")
        for(let k=0;k<buttons.length;k++){
            buttons[k].disabled = reset
            buttons[k].style.background = ""
            buttons[k].classList.remove("selected")
        }
        hour.value = ""
        day.value = ""
    }
    const TeacherSelect = document.getElementById("teacher")
    function changeTimetable(){
        const selectedClass = TeacherSelect;
        console.log(getSelectValues(selectedClass))
        getSelectValues(selectedClass).forEach((element) => {
        const url = `/getClasses/${element}`;
        console.log(selectedClass)
        fetch(url)
        .then(response => response.json())
        .then(data => {
        data.classesTimes.forEach((branch) => {
            console.log(branch.day + "-" + branch.hour)
            const doc = document.getElementById(branch.day + "-" + branch.hour)
            doc.disabled = true
            doc.style.background = "lightgrey";
        })})})}
        markClasses()
    TeacherSelect.addEventListener('change', (event) => resetBoard(false))
    TeacherSelect.addEventListener('change', (event) => markClasses())
    TeacherSelect.addEventListener('change', (event) => changeTimetable(event))
    let day
    let hour
    hourField = document.getElementById("hour")
    dayField = document.getElementById("day")
    const RoomSelect = document.getElementById("room")
    let options = RoomSelect.options;
    function getOptionByText (a) {
        for (let i = 0; i < options.length; i++) {
            if (Number(options[i].value) === a) {
                return options[i]
            }
        }
        return null
    }
    function ButtonClick(test){
        RoomSelect.disabled=false;
        buttons = document.getElementsByTagName("button")
        for(let i=0;i<buttons.length;i++){
            buttons[i].classList.remove("selected")
        }
        for (let i = 0; i < options.length; i++) {
            options[i].hidden = false
        }
        RoomSelect.selectedIndex = 0
        test.classList.add("selected");
        [day , hour] = test.id.split("-")
        hourField.value = hour
        dayField.value = day
        fetch(`/getRoom/?hour=${hour}&day=${day}`)
        .then(response => response.json())
        .then(data => {
        data.availableRooms.forEach((branch) => {
            getOptionByText(branch.id).hidden = true
        })})
    }


    const button_2 = document.getElementsByTagName("button")
    const teacherSelectCont = document.getElementsByClassName("dropdown")
    const CheckBox = document.getElementById("isAStudentTeaching")
    const studentTeacherInput = document.getElementById("studentTeaching")
    function toggleTeacherStudent(checkbox){
        if (CheckBox.checked){
            teacherSelectCont[0].hidden = "none";
            TeacherSelect.value =""
            studentTeacherInput.required = true
            studentTeacherInput.hidden = false;
            resetBoard(false)
        }
        else {
            studentTeacherInput.required = false;
            teacherSelectCont[0].hidden = false;
            studentTeacherInput.hidden = true;
            resetBoard(true)
        }
        markClasses()
    }
