function loadInquiries(){

fetch("/api/inquiries")
.then(res=>res.json())
.then(data=>{

inquiryTable.innerHTML="";

data.forEach(i=>{
inquiryTable.innerHTML+=`
<tr>
<td>${i.customer_name}</td>
<td>${i.budget}</td>
<td>${i.city}</td>
<td>${i.type}</td>
<td><span class="badge bg-warning text-dark">${i.status}</span></td>
<td>
<button class="btn btn-warning btn-sm"
onclick='viewInquiry(${JSON.stringify(i)})'
data-bs-toggle="modal"
data-bs-target="#inquiryModal">
View
</button>
</td>
</tr>
`;
});

});
}

function viewInquiry(i){

inquiryDetails.innerHTML=`
<h6>Customer Info</h6>
<p><b>Name:</b> ${i.customer_name}</p>
<p><b>WhatsApp:</b> ${i.whatsapp}</p>

<hr>

<h6>Requirement</h6>

<div class="row mb-3">
<div class="col-md-3"><b>City:</b> ${i.city}</div>
<div class="col-md-3"><b>Area:</b> ${i.area}</div>
<div class="col-md-3"><b>Budget:</b> ${i.budget}</div>
<div class="col-md-3"><b>Type:</b> ${i.type}</div>
</div>

<hr>

<h6>Recommended Properties</h6>

<table class="table">
<thead>
<tr>
<th>Property</th>
<th>Price</th>
</tr>
</thead>

<tbody>
${i.recommendations.map(p=>`
<tr>
<td>${p.name}</td>
<td>${p.price}</td>
</tr>
`).join("")}
</tbody>

</table>
`;
}
