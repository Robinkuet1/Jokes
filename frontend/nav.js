(async()=>{
    const rawdata = await fetch("https://jokesapi.robinkuet1.com/categories")
    const data = await rawdata.json();

    data.forEach(element => {
        const container = document.getElementById("categories");
        const divElement = document.createElement("ul");
        divElement.innerHTML = `
        <li><a href="index.html?category=${element[1]}">${element[1]}</a></li>
        `
        container.appendChild(divElement);
    });
})()


$("#search").autocomplete({
    source: async function(request, response){
        request = request["term"]
        if(request[0] == "j" && request[1] == "/"){
            //jokes

        }else if(request[0] == "u" && request[1] == "/")
        {
            //users
            const raw = await fetch("https://jokesapi.robinkuet1.com/autocomplete/users?name="+String(request).substring(2));
            let data = await raw.json();
            for(let i = 0; i < data.length; i++){
                data[i] = "u/"+data[i];
            }
            response(data);
        }else if(request[0] == "c" && request[1] == "/")
        {
            //category
            const raw = await fetch("https://jokesapi.robinkuet1.com/autocomplete/topics?name="+String(request).substring(2));
            let data = await raw.json();
            for(let i = 0; i < data.length; i++){
                data[i] = "c/"+data[i];
            }
            response(data);
        }else
        {
            //category
            const raw = await fetch("https://jokesapi.robinkuet1.com/autocomplete/topics?name="+String(request));
            let data = await raw.json();
            for(let i = 0; i < data.length; i++){
                data[i] = "c/"+data[i];
            }
            response(data);
        }
    },
    minLength: 1,
    select: function (event, ui) {
        console.log(ui.item.value);
    }
});
