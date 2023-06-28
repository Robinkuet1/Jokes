


$("#search").autocomplete({
    source: async function (request, response) {
        request = request["term"]
        if (request[0] == "u" && request[1] == "/") {
            //users
            const raw = await fetch("https://jokesapi.robinkuet1.com/autocomplete/users?name=" + String(request).substring(2));
            let data = await raw.json();
            for (let i = 0; i < data.length; i++) {
                data[i] = "u/" + data[i];
            }
            response(data);
        } else if (request[0] == "c" && request[1] == "/") {
            //category
            const raw = await fetch("https://jokesapi.robinkuet1.com/autocomplete/topics?name=" + String(request).substring(2));
            let data = await raw.json();
            for (let i = 0; i < data.length; i++) {
                data[i] = "c/" + data[i];
            }
            response(data);
        } else {
            //category
            const raw = await fetch("https://jokesapi.robinkuet1.com/autocomplete/topics?name=" + String(request));
            let data = await raw.json();
            for (let i = 0; i < data.length; i++) {
                data[i] = "c/" + data[i];
            }
            response(data);
        }
    },
    minLength: 1,
    select: function (event, ui) {
        const text = ui.item.value;
        if (text[0] == "u") {
            window.location = "index.html?user="+String(text).substring(2);
        }
        else if (text[0] == "c") {
            window.location = "index.html?category="+String(text).substring(2);
        }
    }
});
