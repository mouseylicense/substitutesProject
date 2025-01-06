const classesByHour = JSON.parse(document.getElementById("ClassesByHour").textContent)
const rooms = JSON.parse(document.getElementById("rooms").textContent)
    console.log(rooms)
console.log(classesByHour)
const eleven_row = document.getElementById("eleven-row")
const filtering = document.getElementsByClassName("filtering")[0]
const classesTab = document.getElementById("classes-tab")
const roomsTab = document.getElementById("free-tab")
const timeframes = document.getElementsByClassName("timeframe")
    const modalContent = document.getElementById("modal-content")
    const modal = document.getElementById("myModal");
    const span = document.getElementsByClassName("close")[0];
    function markClasses(){
        Object.keys(classesByHour).forEach(function(key) {
            if(key.slice(-5) === "11:00"){
                eleven_row.style.display = "block"
            }
           let div = document.getElementById(key)
            for(let i = 0; i<classesByHour[key].length;i++){
                let new_element = document.createElement("button")
                new_element.innerText = classesByHour[key][i]["name"] + " - " + classesByHour[key][i]["teacher"] + " - " + classesByHour[key][i]["grades_display"] + " - " + classesByHour[key][i]["room"];
                new_element.dataset.name = classesByHour[key][i]["name"];
                new_element.className = "class"
                new_element.dataset.room = classesByHour[key][i]["room"];
                new_element.dataset.teacher = classesByHour[key][i]["teacher"];
                new_element.dataset.grades = classesByHour[key][i]["grades_display"];
                new_element.dataset.hour = key.slice(-5)
                new_element.dataset.description = classesByHour[key][i]["description"]
                new_element.dataset.all_grades = classesByHour[key][i]["all_grades"];
                new_element.setAttribute("onclick","setModalContent(this);")
                div.append(new_element)
            }
        });
        }

        function setModalContent(element){
            modal.style.display = "block";
            modalContent.querySelector("#name-and-grades").innerText = element.dataset.name + " - " + element.dataset.grades;
            modalContent.querySelector("#teacher").innerText = element.dataset.teacher
            modalContent.querySelector("#room").innerText = element.dataset.room
            modalContent.querySelector("#hour").innerText = element.dataset.hour
            modalContent.querySelector("#description").innerText = element.dataset.description
            modal.style.display = "block";
        }



    // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
          modal.style.display = "none";
        }
        markClasses()

function classTabClick(){
        filtering.style.pointerEvents = "unset";
        filtering.style.maxWidth = "10%"
        clearAll()
        markClasses()
        roomsTab.classList.remove("selectedtab");
        classesTab.classList.add("selectedtab");
}
function roomsTabClick(){
        uncheck()
        classesTab.classList.remove("selectedtab");
        roomsTab.classList.add("selectedtab");
        filtering.style.pointerEvents = "none"
        filtering.style.maxWidth = "1%";
        clearAll()
        for(let i=0; i<timeframes.length; i++){
            const unavailable_rooms = []
            console.log(timeframes[i].id);
            if(classesByHour[timeframes[i].id] !== undefined){
            for(let k=0;k<classesByHour[timeframes[i].id].length;k++){
                unavailable_rooms.push(classesByHour[timeframes[i].id][k].room);
            }
            for(let j=0; j<rooms.length;j++){
                if(!unavailable_rooms.includes(rooms[j])){
                    let new_element = document.createElement("button")
                    new_element.innerText = rooms[j];
                    new_element.className = "class"
                    timeframes[i].appendChild(new_element)
            }}}
            else{
               for(let j=0; j<rooms.length;j++){
                    let new_element = document.createElement("button")
                    new_element.innerText = rooms[j];
                    new_element.className = "class"
                    timeframes[i].appendChild(new_element)
            }

        }

}}

function uncheck(){
    teacher.value=""
    for(const checkbox of checkboxes){
        if(checkbox.checked){
            checkbox.checked=false

        }
    }
    filterTeachers()
    filterGrades()
}
function clearAll(){
        for(let i = 0;i<timeframes.length;i++){
            while (timeframes[i].firstChild){
                timeframes[i].removeChild(timeframes[i].lastChild)
            }
        }
}