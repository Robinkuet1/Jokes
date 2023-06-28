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

    if(localStorage.id)
        url += `userId=${localStorage.id}&`

    if (sort)
        url += `&order=${sort}`
    else
        url += `&order=new`

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
        let userUpVote = 0;
        let userDownVote = 0;

        if(localStorage.id){
            userUpVote = element[10];
            userDownVote = element[11];
        }

        divElement.addEventListener
        divElement.innerHTML = `
        <div class="">
            <div class="content container">
                <div>
                    <div class="vote-container">
                        <img src="images/${userUpVote ? "up-vote-icon.png" : "up-vote-icon-empty.png"}" id="upvote${id}" class="vote">
                        <p class="vote">${upvotes}</p>
                        <img src="images/${userDownVote ? "down-vote-icon.png" : "down-vote-icon-empty.png"}" id="downvote${id}" class="vote">
                    </div>
                </div>
                <div>
                    <div style="display: flex;" class="joke-header">
                        <div style="padding-right: 0.4em !important; font-size: 0.9em">c/${categoryName} •</div><div style="font-size: 0.7em">Posted by ${username}  </div><img class="joke-header" width="auto" height="12px" style="margin: 0 3px ! important" alt="${countryName}" src="https://flagicons.lipis.dev/flags/4x3/${countryCode.toLowerCase()}.svg"/><div  style="font-size: 0.7em">on ${date}</div>
                    </div>
                    <div>
                        <p class="text">
                        ${text}
                        </p>
                        <br>
                    </div>
                    <!--  joke-header<div>by ${username} <img width=25 height=20 alt="${countryName}" src="https://flagicons.lipis.dev/flags/4x3/${countryCode.toLowerCase()}.svg"/> in ${categoryName} on ${date}</div> -->
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

        document.getElementById(`upvote${id}`).addEventListener("click", async function () {
            if (checkLogin()) {
                if (String(document.getElementById(`upvote${id}`).src).includes("empty")) {
                    document.getElementById(`upvote${id}`).src = upvoteIcon;
                    document.getElementById(`downvote${id}`).src = downvoteIconEmpty;

                    await fetch(`https://jokesapi.robinkuet1.com/upvote?userId=${localStorage.id}&userToken=${localStorage.token}&jokeId=${id}&up=1`);
                    window.location.reload();
                }
                else{
                    document.getElementById(`upvote${id}`).src = upvoteIconEmpty;
                    await fetch(`https://jokesapi.robinkuet1.com/upvote?userId=${localStorage.id}&userToken=${localStorage.token}&jokeId=${id}`);
                    window.location.reload();
                }
                console.log("upvote");
            }
        });

        document.getElementById(`downvote${id}`).addEventListener("click", async function () {
            if (checkLogin()) {
                if (String(document.getElementById(`downvote${id}`).src).includes("empty")) {
                    document.getElementById(`downvote${id}`).src = downvoteIcon;
                    document.getElementById(`upvote${id}`).src = upvoteIconEmpty;

                    await fetch(`https://jokesapi.robinkuet1.com/upvote?userId=${localStorage.id}&userToken=${localStorage.token}&jokeId=${id}&up=0`);
                    window.location.reload();
                }
                else
                {
                    document.getElementById(`downvote${id}`).src = downvoteIconEmpty;

                    await fetch(`https://jokesapi.robinkuet1.com/upvote?userId=${localStorage.id}&userToken=${localStorage.token}&jokeId=${id}`);
                    window.location.reload();
                }
                console.log("downvote");
            }
        });
    });
})()
