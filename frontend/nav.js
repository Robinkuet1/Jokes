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
