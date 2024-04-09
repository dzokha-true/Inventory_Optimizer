const object = document.getElementById("")

const insertData = (newData) =>{
    fetch('http://localhost:5000/get',{
        method:'POST',
        headers: {

        },
        body:JSON.stringify(newData)
    })
    .then(resp => resp.json())
    .then((data) => {
        console.log(data)
    })
    .catch(error => console.log(error))
}

object.addEventListener('submit',(e)=>{
    e.preventDefault()

    const newData={
        title:title.value,
        body:body.value
    }

    insertData(newData)
})