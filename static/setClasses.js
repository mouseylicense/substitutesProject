const classesByHour = JSON.parse(document.getElementById("ClassesByHour").textContent)
        function markClasses(){
        Object.keys(classesByHour).forEach(function(key) {
           let button = document.getElementById(key)
            button.style.background = `rgba(195, 201, 83,${classesByHour[key]/7.5})`;
            button.innerText = classesByHour[key]
        });
        }
    function resetBoard(reset){
        const hour = document.getElementById("hour")
        const day = document.getElementById("day")
        const buttons = document.getElementsByTagName("button")
        for(let k=0;k<buttons.length;k++){
            buttons[k].disabled = reset
            buttons[k].style.background = ""
            buttons[k].className = ""
        }
        hour.value = ""
        day.value = ""
    }
    const TeacherSelect = document.getElementById("teacher")
    function changeTimetable(){
        const selectedClass = TeacherSelect;
        const url = `/getClasses/${selectedClass.value}`;
        console.log(selectedClass)
        fetch(url)
        .then(response => response.json())
        .then(data => {
        data.classesTimes.forEach((branch) => {
            console.log(branch.day + "-" + branch.hour)
            const doc = document.getElementById(branch.day + "-" + branch.hour)
            doc.disabled = true
            doc.style.background = "lightgrey";
        })})}
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
            buttons[i].className = ""
        }
        for (let i = 0; i < options.length; i++) {
            options[i].hidden = false
        }
        RoomSelect.selectedIndex = 0
        test.className = "selected";
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
    const teacherSelect = document.getElementById("teacher")
    const CheckBox = document.getElementById("isAStudentTeaching")
    const studentTeacherInput = document.getElementById("studentTeaching")
    function toggleTeacherStudent(checkbox){
        if (CheckBox.checked){
            teacherSelect.hidden = true;
            teacherSelect.value =""
            studentTeacherInput.required = true
            studentTeacherInput.hidden = false;
            resetBoard(false)
        }
        else {
            studentTeacherInput.required = false;
            teacherSelect.hidden = false;
            studentTeacherInput.hidden = true;
            resetBoard(true)
        }
        markClasses()
    }
