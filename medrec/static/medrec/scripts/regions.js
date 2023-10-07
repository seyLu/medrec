const provincesDatalist = document.getElementById("province-datalist");
const citiesDatalist = document.getElementById("city-datalist");
const districtsDatalist = document.getElementById("district-datalist");

DATALIST_MAP = {
    "provinces": provincesDatalist,
    "cities": citiesDatalist,
    "districts": districtsDatalist
}

async function getProvinceEndpoint(endpoint="provinces") {
    const res = await fetch("provinces/", {
        method: "POST",
        headers: {
            "X-CSRFToken": CSRF_TOKEN,
        },
        mode: "same-origin",
    });
    const items = await res.json();

    DATALIST_MAP[endpoint].innerHTML = "";

    for (item of items) {
        const option = document.createElement("option");
        option.value = item.name;
        option.innerHTML = item.code;
        option.dataset.code = item.code;

        if (item.region_code) option.dataset.region_code = item.region_code;
        if (item.province_code) option.dataset.province_code = item.province_code;
        if (item.city_code) option.dataset.city_code = item.city_code;
        if (item.district_code) option.dataset.district_code = item.district_code;

        DATALIST_MAP[endpoint].appendChild(option);
    }
}

getProvinceEndpoint();

async function getEndpointName(endpoint, code) {
    const res = await fetch(`${endpoint}/?code=${code}`);
    const item = await res.json();

    return item.name;
}


async function getEndpoint(parent, parent_code, child) {
    const res = await fetch(`${child}/?${parent}=${parent_code}`, {
        method: "POST",
        headers: {
            "X-CSRFToken": CSRF_TOKEN,
        },
        mode: "same-origin",
    });
    const items = await res.json();

    DATALIST_MAP[endpoint].innerHTML = "";

    for (item of items) {
        const option = document.createElement("option");
        option.value = item.name;
        option.innerHTML = item.code;
        option.dataset.code = item.code;

        if (item.region_code) option.dataset.region_code = item.region_code;
        if (item.province_code) option.dataset.province_code = item.province_code;
        if (item.city_code) option.dataset.city_code = item.city_code;
        if (item.district_code) option.dataset.district_code = item.district_code;

        DATALIST_MAP[endpoint].appendChild(option);
    }
}


const provincesInput = document.getElementById("province");
const citiesInput = document.getElementById("city");
const districtsInput = document.getElementById("district");


provincesInput.addEventListener("input", async e => {
    if (!(e instanceof InputEvent) || e.inputType === 'insertReplacementText') {
        const input_val = provincesInput.value;
        const option_val = provincesDatalist.querySelector(`option[value="${input_val}"]`);

        citiesInput.value = "";
        districtsInput.value = "";

        getEndpoint("provinces", option_val.dataset.code, "cities")
        getEndpoint("provinces", option_val.dataset.code, "districts")
    }
});


citiesInput.addEventListener("input", async e => {
    if (!(e instanceof InputEvent) || e.inputType === 'insertReplacementText') {
        const input_val = citiesInput.value;
        const option_val = citiesDatalist.querySelector(`option[value="${input_val}"]`);

        districtsInput.value = "";

        provincesInput.value = await getEndpointName("provinces", option_val.dataset.province_code);
        getEndpoint("cities", option_val.dataset.code, "districts")
    }
});


districtsInput.addEventListener("input", async e => {
    if (!(e instanceof InputEvent) || e.inputType === 'insertReplacementText') {
        const input_val = districtsInput.value;
        const option_val = districtsDatalist.querySelector(`option[value="${input_val}"]`);

        provincesInput.value = await getEndpointName("provinces", option_val.dataset.province_code);
        citiesInput.value = await getEndpointName("cities", option_val.dataset.city_code);
    }
});
