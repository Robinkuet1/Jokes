(async()=>{
    const rawdata = await fetch("https://jokesapi.robinkuet1.com/jokes?limit=1000&category=dark")
    const data = await rawdata.json();

    data.forEach(element => {
        const container = document.getElementById("serb");
        const divElement = document.createElement("div");
        divElement.innerHTML = `
        <div class="content">
            <div>
                <div class="vote-container">

                    <img src="images/vote-icon.png" alt="" class="vote">
                    <p class="vote">${element[3]}</p>
                    <img src="images/down-vote-icon.png" alt="" class="vote">

                </div>
            </div>
            <div>
                <p class="text">
                ${element[1]}
                </p>
                <p>${element[2]}</p>
                <p></p>
                <p>${element[4]}</p>
                <p>${element[5]}</p>
                <p>${element[6]}</p>
                <p>${element[7]}</p>
                <p>${element[8]}</p>
                <br>
            </div>
        </div>
        `
        container.appendChild(divElement);
    });
})()
