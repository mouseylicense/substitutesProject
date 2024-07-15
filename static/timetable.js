const classesByHour = JSON.parse(document.getElementById("ClassesByHour").textContent)
    console.log(classesByHour)

    const modalContent = document.getElementById("modal-content")
    const modal = document.getElementById("myModal");
    const span = document.getElementsByClassName("close")[0];
    function markClasses(){
        Object.keys(classesByHour).forEach(function(key) {
           let div = document.getElementById(key)
            for(let i = 0; i<classesByHour[key].length;i++){
                let new_element = document.createElement("button")
                new_element.innerText = classesByHour[key][i]["name"] + " - " + classesByHour[key][i]["teacher"] + " - " + classesByHour[key][i]["grades"] + " - " + classesByHour[key][i]["room"];
                new_element.dataset.name = classesByHour[key][i]["name"];
                new_element.dataset.room = classesByHour[key][i]["room"];
                new_element.dataset.teacher = classesByHour[key][i]["teacher"];
                new_element.dataset.grades = classesByHour[key][i]["grades"];
                new_element.dataset.hour = key.slice(-5)
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
            modal.style.display = "block";
        }



    // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
          modal.style.display = "none";
        }
        markClasses()