const PREVIEW_BYTES = 5000;

class FileUpload {
    constructor(file) {
        this.file = file;
    }

    _fetchContent(consumeText, previewText = false) {
        let fileUpload = this;
        let reader = new FileReader();
        reader.onload = function (e) {
            let text = reader.result;
            if (previewText) {
                text = fileUpload.formatPreview(text)
            }
            consumeText(text);
        }
        if (previewText) {
            reader.readAsText(this.file.slice(0, PREVIEW_BYTES));
        } else {
            reader.readAsText(this.file);
        }
    }

    fetchAllFile(consumeText) {
        return this._fetchContent(consumeText, false);
    }
}

export default FileUpload;