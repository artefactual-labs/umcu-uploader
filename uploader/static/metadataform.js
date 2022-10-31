//  add new  input field on button click
const addAuthorNameButton = document.querySelector("#add-author");
// select input group for author name
const authorNameInputGroup = document.querySelector(".author-name-group");
// select the remove author name button
const removeAuthorNameButton = document.querySelector("#remove-author");
//  the number of input fields for author name

const addAuthorNameInput = () => {
  const authorDiv = document.createElement("div");
  authorDiv.className = "my-3";
  const authorNameInput = document.createElement("input");
  authorNameInput.title = "author";
  authorNameInput.type = "text";
  authorNameInput.className = "form-control";
  authorDiv.append(authorNameInput);
  authorNameInputGroup.append(authorDiv);
  authorNameInput.name =
  "author" +"-"+ (authorNameInputGroup.childElementCount);
  let authorNameInputCount = authorNameInputGroup.childElementCount;
  // add this behavior as a listener to the input group for author name
  if (authorNameInputCount > 1) {
    removeAuthorNameButton.removeAttribute("hidden");
  }
};
// this function removes the last input field for author name
const removeAuthorNameInput = () => {
  authorNameInputGroup.removeChild(authorNameInputGroup.lastChild);
  let authorNameInputCount = authorNameInputGroup.childElementCount;
  if (authorNameInputCount > 1) {
    removeAuthorNameButton.removeAttribute("hidden");
  } else if (authorNameInputCount === 1) {
    removeAuthorNameButton.hidden = true;
  }
};
// add event listener to add author name button

addAuthorNameButton.addEventListener("click", addAuthorNameInput);

// add event listener to remove author name button
removeAuthorNameButton.addEventListener("click", removeAuthorNameInput);

// --------------------------------------------

//  add new input field on button click for keywords
const addKeywordButton = document.querySelector("#add-keyword");
// select input group for keywords
const keywordInputGroup = document.querySelector(".keyword-name-group");
// select the remove keyword button
const removeKeywordButton = document.querySelector("#remove-keyword");
//  the number of input fields for keywords

const addKeywordInput = () => {
  const keywordDiv = document.createElement("div");
  keywordDiv.className = "my-3";
  const keywordInput = document.createElement("input");
  keywordInput.title = "keyword";
  keywordInput.type = "text";
  keywordInput.className = "form-control";
  keywordDiv.append(keywordInput);
  keywordInputGroup.append(keywordDiv);
  keywordInput.name = "keyword" + (keywordInputGroup.childElementCount - 1);

  let keywordInputCount = keywordInputGroup.childElementCount;
  // add this behavior as a listener to the input group for keywords
  if (keywordInputCount > 1) {
    removeKeywordButton.removeAttribute("hidden");
  }
};
// this function removes the last input field for keywords
const removeKeywordInput = () => {
  keywordInputGroup.removeChild(keywordInputGroup.lastChild);
  let keywordInputCount = keywordInputGroup.childElementCount;
  if (keywordInputCount > 1) {
    removeKeywordButton.removeAttribute("hidden");
  } else if (keywordInputCount === 1) {
    removeKeywordButton.hidden = true;
  }
};
// add event listener to add keyword button

addKeywordButton.addEventListener("click", addKeywordInput);

// add event listener to remove keyword button
removeKeywordButton.addEventListener("click", removeKeywordInput);

// --------------------------------------------
//  add new input field on button click contact
const addContactButton = document.querySelector("#add-contact");
// select input group for contact
const contactInputGroup = document.querySelector(".contact-group");
// select the remove contact button
const removeContactButton = document.querySelector("#remove-contact");
//  the number of input fields for contact

const addContactInput = () => {
  const contactDiv = document.createElement("div");
  contactDiv.className = "my-3";
  contactDiv.classList.add("input-group");
  const contactNameSpan = document.createElement("span");
  contactNameSpan.className = "input-group-text";
  contactNameSpan.innerText = "Name";
  const contactEmailSpan = document.createElement("span");
  contactEmailSpan.className = "input-group-text";
  contactEmailSpan.innerText = "Email";
  const contactNameInput = document.createElement("input");
  contactNameInput.title = "contact-name";
  contactNameInput.type = "text";
  contactNameInput.name = "contact-name";
  contactNameInput.className = "form-control";

  const contactEmailInput = document.createElement("input");
  contactEmailInput.title = "contact";
  contactEmailInput.type = "text";
  contactEmailInput.name =
    "contact-email" + (contactInputGroup.childElementCount - 1);
  contactEmailInput.className = "form-control";
  contactDiv.append(contactNameSpan);
  contactDiv.append(contactNameInput);
  contactDiv.append(contactEmailSpan);
  contactDiv.append(contactEmailInput);
  contactInputGroup.append(contactDiv);

  let contactInputCount = contactInputGroup.childElementCount;
  // add this behavior as a listener to the input group for contact
  if (contactInputCount > 1) {
    removeContactButton.removeAttribute("hidden");
  }
};
// this function removes the last input field for contact
const removeContactInput = () => {
  contactInputGroup.removeChild(contactInputGroup.lastChild);
  let contactInputCount = contactInputGroup.childElementCount;
  if (contactInputCount > 1) {
    removeContactButton.removeAttribute("hidden");
  } else if (contactInputCount === 1) {
    removeContactButton.hidden = true;
  }
};
// add event listener to add contact button

addContactButton.addEventListener("click", addContactInput);

// add event listener to remove contact button
removeContactButton.addEventListener("click", removeContactInput);

// ---------------------
// set current date as the value of the data deposit date
const depositDateInput = document.querySelector("#deposit-datename");
currentDate = new Date(Date.now());

depositDateInput.setAttribute("value", currentDate.toISOString().slice(0, 10));

// ---------------------
// add new input field on button click for related publication
const addRelatedPublicationButton = document.querySelector(
  "#add-related-publication"
);
const relatedPublicationInputGroup = document.querySelector(
  ".related-publication-group"
);
const removeRelatedPublicationButton = document.querySelector(
  "#remove-related-publication"
);

const addRelatedPublicationInput = () => {
  const relatedPublicationDiv = document.createElement("div");
  relatedPublicationDiv.className = "my-3";
  const relatedPublicationInput = document.createElement("input");
  relatedPublicationInput.title = "related-publication";
  relatedPublicationInput.type = "text";
  relatedPublicationInput.name =
    "related-publication" +
    (relatedPublicationInputGroup.childElementCount - 1);
  relatedPublicationInput.className = "form-control";
  relatedPublicationDiv.append(relatedPublicationInput);
  relatedPublicationInputGroup.append(relatedPublicationDiv);

  let relatedPublicationInputCount =
    relatedPublicationInputGroup.childElementCount;
  // add this behavior as a listener to the input group for related publication
  if (relatedPublicationInputCount > 1) {
    removeRelatedPublicationButton.removeAttribute("hidden");
  }
};

const removeRelatedPublicationInput = () => {
  relatedPublicationInputGroup.removeChild(
    relatedPublicationInputGroup.lastChild
  );
  let relatedPublicationInputCount =
    relatedPublicationInputGroup.childElementCount;
  if (relatedPublicationInputCount > 1) {
    removeRelatedPublicationButton.removeAttribute("hidden");
  } else if (relatedPublicationInputCount === 1) {
    removeRelatedPublicationButton.hidden = true;
  }
};

addRelatedPublicationButton.addEventListener(
  "click",
  addRelatedPublicationInput
);

removeRelatedPublicationButton.addEventListener(
  "click",
  removeRelatedPublicationInput
);

// ---------------------
// add new input field on button click for related publication
const addContributorButton = document.querySelector("#add-contributor");
const ContributorInputGroup = document.querySelector(".contributor-group");
const removeContributorButton = document.querySelector("#remove-contributor");

const addContributorInput = () => {
  const ContributorDiv = document.createElement("div");
  ContributorDiv.className = "my-3";
  const ContributorInput = document.createElement("input");
  ContributorInput.title = "contributor";
  ContributorInput.type = "text";
  ContributorInput.name =
    "contributor" + (ContributorInputGroup.childElementCount - 1);
  ContributorInput.className = "form-control";
  ContributorDiv.append(ContributorInput);
  ContributorInputGroup.append(ContributorDiv);

  let ContributorInputCount = ContributorInputGroup.childElementCount;
  // add this behavior as a listener to the input group for related publication
  if (ContributorInputCount > 1) {
    removeContributorButton.removeAttribute("hidden");
  }
};

const removeContributorInput = () => {
  ContributorInputGroup.removeChild(ContributorInputGroup.lastChild);
  let ContributorInputCount = ContributorInputGroup.childElementCount;
  if (ContributorInputCount > 1) {
    removeContributorButton.removeAttribute("hidden");
  } else if (ContributorInputCount === 1) {
    removeContributorButton.hidden = true;
  }
};

addContributorButton.addEventListener("click", addContributorInput);

removeContributorButton.addEventListener("click", removeContributorInput);
// ---------------------
// add new input field on button click for related publication
const addSoftwareButton = document.querySelector("#add-software");
const SoftwareInputGroup = document.querySelector(".software-group");
const removeSoftwareButton = document.querySelector("#remove-software");

const addSoftwareInput = () => {
  const SoftwareDiv = document.createElement("div");
  SoftwareDiv.className = "my-3";
  const SoftwareInput = document.createElement("input");
  SoftwareInput.title = "Software";
  SoftwareInput.type = "text";
  SoftwareInput.name = "software" + (SoftwareInputGroup.childElementCount - 1);
  SoftwareInput.className = "form-control";
  SoftwareDiv.append(SoftwareInput);
  SoftwareInputGroup.append(SoftwareDiv);

  let SoftwareInputCount = SoftwareInputGroup.childElementCount;
  // add this behavior as a listener to the input group for related publication
  if (SoftwareInputCount > 1) {
    removeSoftwareButton.removeAttribute("hidden");
  }
};

const removeSoftwareInput = () => {
  SoftwareInputGroup.removeChild(SoftwareInputGroup.lastChild);
  let SoftwareInputCount = SoftwareInputGroup.childElementCount;
  if (SoftwareInputCount > 1) {
    removeSoftwareButton.removeAttribute("hidden");
  } else if (SoftwareInputCount === 1) {
    removeSoftwareButton.hidden = true;
  }
};

addSoftwareButton.addEventListener("click", addSoftwareInput);

removeSoftwareButton.addEventListener("click", removeSoftwareInput);
// ---------------------
// add new input field on button click for related publication
const addLanguageButton = document.querySelector("#add-language");
const LanguageInputGroup = document.querySelector(".language-group");
const removeLanguageButton = document.querySelector("#remove-language");

const addLanguageInput = () => {
  const LanguageDiv = document.createElement("div");
  LanguageDiv.className = "my-3";
  const LanguageInput = document.createElement("input");
  LanguageInput.title = "Language";
  LanguageInput.type = "text";
  LanguageInput.name = "language" + (LanguageInputGroup.childElementCount - 1);
  LanguageInput.className = "form-control";
  LanguageDiv.append(LanguageInput);
  LanguageInputGroup.append(LanguageDiv);

  let LanguageInputCount = LanguageInputGroup.childElementCount;
  // add this behavior as a listener to the input group for related publication
  if (LanguageInputCount > 1) {
    removeLanguageButton.removeAttribute("hidden");
  }
};

const removeLanguageInput = () => {
  LanguageInputGroup.removeChild(LanguageInputGroup.lastChild);
  let LanguageInputCount = LanguageInputGroup.childElementCount;
  if (LanguageInputCount > 1) {
    removeLanguageButton.removeAttribute("hidden");
  } else if (LanguageInputCount === 1) {
    removeLanguageButton.hidden = true;
  }
};

addLanguageButton.addEventListener("click", addLanguageInput);

removeLanguageButton.addEventListener("click", removeLanguageInput);
