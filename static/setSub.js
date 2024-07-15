const ClassSelect = document.getElementById('sub');
        const TeacherSelect = document.getElementById('teacher');


        function changeOptions(event){
        const selectedClass = ClassSelect.value;
        const url = `/get/${selectedClass}`;
        console.log(selectedClass)
        fetch(url)
        .then(response => response.json())
        .then(data => {
        TeacherSelect.innerHTML = '';
        console.log(data)
        data.availableTeachers.forEach((branch) => {
        const option = document.createElement('option');
        option.value = branch.id;
        option.text = branch.name;
        TeacherSelect.appendChild(option);

        })});
        }
        changeOptions()
        ClassSelect.addEventListener('change', (event) => changeOptions(event))