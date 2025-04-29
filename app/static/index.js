// Get the root element
const r = document.querySelector(':root');
const periwinkle = getComputedStyle(r).getPropertyValue('--periwinkle');
const richBlack = getComputedStyle(r).getPropertyValue('--rich-black');

document.addEventListener('drop', (ev) => {
  ev.preventDefault();
})
document.addEventListener('dragover', (ev) => {
  ev.preventDefault();
})

// drop box events
const drop_box = document.querySelector('.drop_zone');
drop_box.addEventListener('drop', dropHandler, false);
drop_box.addEventListener('dragover', dragOverHandler);
drop_box.addEventListener('dragleave', dragLeaveHandler); 


function dropHandler(e) {
  console.log("File(s) dropped");
  lightMode(drop_box);

  // Prevent default behavior (Prevent file from being opened)
  e.preventDefault();

  let dt = e.dataTransfer;
  let files = dt.files;
  if (files.length) {
    uploadFile(files[0]);
  }
};

function uploadFile(file) {
  let formData = new FormData();
  formData.append('file', file);

  fetch('/', {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (response.redirected) {
      window.location.href = response.url;  // Redirect to the labeling page
    } else {
      alert('Upload failed.');
    }
  })
  .catch(() => {
    alert('Upload failed.');
  });
}

function dragOverHandler(ev) {
  console.log("File(s) in drop zone");
  drop_box.textContent = 'Upload it';
  darkMode(drop_box);
  drop_box.style.border = '8px solid var(--periwinkle)';
  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault();
}

function dragLeaveHandler() {
  drop_box.textContent = 'Drop a File';
  lightMode(drop_box);
}

function lightMode(targetElement) {
  targetElement.style.backgroundColor = periwinkle;
  targetElement.style.color = 'black';
}

function darkMode(targetElement) {
  targetElement.style.backgroundColor = richBlack;
  targetElement.style.color = 'white';
}

// file upload events
const input = document.querySelector("input");
const input_name = document.querySelector(".input-file-name");
const input_size = document.querySelector(".input-file-size");
input.addEventListener("change", updateImageDisplay);

function updateImageDisplay() {
  const curFiles = input.files;
  if (curFiles.length === 0) {
    input_name.textContent = "No files currently selected for upload";
  } else {
    input_name.textContent = `File name: ${curFiles[0].name}`;
    input_size.textContent = `File size: ${returnFileSize(curFiles[0].size)}`;
  }
}

function returnFileSize(number) {
  if (number < 1e3) {
    return `${number} bytes`;
  } else if (number >= 1e3 && number < 1e6) {
    return `${(number / 1e3).toFixed(1)} KB`;
  } else {
    return `${(number / 1e6).toFixed(1)} MB`;
  }
}