"use strict";

class InputIncrementer {
  constructor(
    addButton,
    removeButton,
    inputGroup,
    name,
    title = name,
    type = "text"
  ) {
    this.addButton = addButton;
    this.removeButton = removeButton;
    this.inputGroup = inputGroup;
    this.name = name;
    this.title = title;
    this.type = type;
  }
  addInput = () => {
    const div = document.createElement("div");
    div.className = "my-3";
    const input = document.createElement("input");
    input.title = this.title;
    input.type = this.type;
    input.className = "form-control";
    div.append(input);
    this.inputGroup.append(div);
    input.name = title + "-" + (this.inputGroup.childElementCount - 1);
    let inputCount = this.inputGroup.childElementCount;
    if (inputCount > 1) this.removeButton.removeAttribute("hidden");
  };
  removeInput = () => {
    this.inputGroup.removeChild(this.inputGroup.lastChild);
    let inputCount = this.inputGroup.childElementCount;
    if (inputCount > 1) {
      this.removeButton.removeAttribute("hidden");
    } else if (inputCount === 1) {
      this.removeButton.hidden = true;
    }
  };
}
//  add new  input field on button click
const addAuthorNameButton = document.querySelector("#add-author");
// select input group for author name
const authorNameInputGroup = document.querySelector(".author-name-group");
// select the remove author name button
const removeAuthorNameButton = document.querySelector("#remove-author");
//  the number of input fields for author name
const authorIncrementer = new InputIncrementer(
  addAuthorNameButton,
  removeAuthorNameButton,
  authorNameInputGroup,
  "author",
);

// const addAuthorNameInput = () =>
//   authorIncrementer.addInput();
// this function removes the last input field for author name
// const removeAuthorNameInput = () => authorIncrementer.removeInput();
// add event listener to add author name button

addAuthorNameButton.addEventListener("click", authorIncrementer.removeInput());

// add event listener to remove author name button
removeAuthorNameButton.addEventListener("click", authorIncrementer.addInput());
// --------------------------------------------

//  add new input field on button click for keywords
const addKeywordButton = document.querySelector("#add-keyword");
// select input group for keywords
const keywordInputGroup = document.querySelector(".keyword-name-group");
// select the remove keyword button
const removeKeywordButton = document.querySelector("#remove-keyword");
//  the number of input fields for keywords
const keywordIncrementer = new InputIncrementer(
  addKeywordButton,
  removeKeywordButton,
  keywordInputGroup,
  "keyword",
);
// const addKeywordInput = () => keywordIncrementer.addInput;
// this function removes the last input field for keywords
// const removeKeywordInput = () => keywordIncrementer.removeInput;
// add event listener to add keyword button

addKeywordButton.addEventListener("click",  keywordIncrementer.addInput);

// add event listener to remove keyword button
// removeKeywordButton.addEventListener("click", removeKeywordInput);

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
  contactNameInput.className = "form-control";

  const contactEmailInput = document.createElement("input");
  contactEmailInput.title = "contact";
  contactEmailInput.type = "text";
  contactEmailInput.className = "form-control";
  contactDiv.append(contactNameSpan);
  contactDiv.append(contactNameInput);
  contactDiv.append(contactEmailSpan);
  contactDiv.append(contactEmailInput);
  contactInputGroup.append(contactDiv);
  contactNameInput.name =
    "datasetContactName" + "-" + (contactInputGroup.childElementCount - 1);
  contactEmailInput.name =
    "datasetContactEmail" + "-" + (contactInputGroup.childElementCount - 1);

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
let currentDate = new Date(Date.now());

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

// this function adds a new input field for related publication
const addRelatedPublicationInput = () => {
  const relatedPublicationDiv = document.createElement("div");
  relatedPublicationDiv.className = "my-3";
  const relatedPublicationInput = document.createElement("input");
  relatedPublicationInput.title = "related-publication";
  relatedPublicationInput.type = "text";
  relatedPublicationInput.className = "form-control";
  relatedPublicationDiv.append(relatedPublicationInput);
  relatedPublicationInputGroup.append(relatedPublicationDiv);
  relatedPublicationInput.name =
    "related-publication" +
    "-" +
    (relatedPublicationInputGroup.childElementCount - 1);

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
  ContributorInput.className = "form-control";
  ContributorDiv.append(ContributorInput);
  ContributorInputGroup.append(ContributorDiv);
  ContributorInput.name =
    "contributor" + "-" + (ContributorInputGroup.childElementCount - 1);

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
  SoftwareInput.className = "form-control";
  SoftwareDiv.append(SoftwareInput);
  SoftwareInputGroup.append(SoftwareDiv);
  SoftwareInput.name =
    "software" + "-" + (SoftwareInputGroup.childElementCount - 1);

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
