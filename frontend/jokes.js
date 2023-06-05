(async()=>{
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get("category");
    const sort = urlParams.get("sort")

    let url = "https://jokesapi.robinkuet1.com/jokes?limit=100&"
    if(category)
        url += `category=${category}&`
    if(sort)
        url += `sort=${sort}&`


    const rawdata = await fetch(url)
    const data = await rawdata.json();

    const container = document.getElementById("serb");
    data.forEach(element => {
        const divElement = document.createElement("div");

        const id = element[0];
        const text = element[1];
        const date = element[2];
        const upvotes = Number(element[3]) - Number(element[4]);
        const categoryName = element[5];
        const username = element[6];
        const userId = element[7];
        const countryName = element[8];
        const countryCode = String(element[9]);

        divElement.innerHTML = `
        <div>
            <div class="content">
                <div>
                    <div class="vote-container">
                        <img src="images/vote-icon.png" alt="" class="vote">
                        <p class="vote">${upvotes}</p>
                        <img src="images/down-vote-icon.png" alt="" class="vote">

                    </div>
                </div>
                <div>
                <div>
                    <p class="text">
                    ${text}
                    </p>
                    <br>
                </div>
                <div>by ${username} <img width=25 height=20 alt="${countryName}" src="https://flagicons.lipis.dev/flags/4x3/${countryCode.toLowerCase()}.svg"/> in ${categoryName} on ${date}</div>
                </div>
            </div>
        </div>
        `
        container.appendChild(divElement);
    });
})()
