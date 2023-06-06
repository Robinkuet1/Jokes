(async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const category = urlParams.get("category");
    const sort = urlParams.get("sort")
    const user = urlParams.get("user")

    let url = "https://jokesapi.robinkuet1.com/jokes?limit=100&"
    if (category)
        url += `category=${category}&`
    if (user)
        url += `user=${user}&`
    if (sort)
        url += `order=${sort}`
    console.log(url)


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
        const userUpVote = false;
        const userDownVote = false;
        divElement.addEventListener
        divElement.innerHTML = `
        <div>
            <div class="content">
                <div>
                    <div class="vote-container">
                        <img src="images/${userUpVote ? "up-vote-icon.png" : "up-vote-icon-empty.png"}" id="upvote${id}" class="vote">
                        <p class="vote">${upvotes}</p>
                        <img src="images/${userDownVote ? "down-vote-icon.png" : "down-vote-icon-empty.png"}" id="downvote${id}" class="vote">
                            
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

        function checkLogin() {
            if (!localStorage.id || !localStorage.token) {
                alert("you must log in befor you can vote");
                return false;
            }
            return true;
        }

        const upvoteIcon = "images/up-vote-icon.png";
        const upvoteIconEmpty = "images/up-vote-icon-empty.png";

        const downvoteIcon = "images/down-vote-icon.png";
        const downvoteIconEmpty = "images/down-vote-icon-empty.png";

        document.getElementById(`upvote${id}`).addEventListener("click", function () {
            if (checkLogin()) {
                if (String(document.getElementById(`upvote${id}`).src).includes("empty")) {
                    document.getElementById(`upvote${id}`).src = upvoteIcon;
                    document.getElementById(`downvote${id}`).src = downvoteIconEmpty;
                }
                else
                    document.getElementById(`upvote${id}`).src = upvoteIconEmpty;
                console.log("upvote");
            }
        });

        document.getElementById(`downvote${id}`).addEventListener("click", function () {
            if (checkLogin()) {
                if (String(document.getElementById(`downvote${id}`).src).includes("empty")) {
                    document.getElementById(`downvote${id}`).src = downvoteIcon;
                    document.getElementById(`upvote${id}`).src = upvoteIconEmpty;
                }
                else
                    document.getElementById(`downvote${id}`).src = downvoteIconEmpty;
                console.log("downvote");
            }
        });
    });
})()
