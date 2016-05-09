import {URL} from './URL.js'

class PredictionsStore {
    constructor(pageBatch, urlBuilder) {
        this.pageBatch = pageBatch;
        this.urlBuilder = urlBuilder;
        this.lastSearchSettingsStr = undefined;
    }

    requestPage(pageNum, searchSettings, onData, onError) {
        this.saveSearchSettings(searchSettings);
        if (this.pageBatch.hasPage(pageNum)) {
            onData(this.pageBatch.getItems(pageNum), pageNum, true, '');
        } else {
            let batchPage = this.pageBatch.getBatchPageNum(pageNum)
            let itemsPerBatch = this.pageBatch.getItemsPerBatch();
            this.setBuilderURL(batchPage, itemsPerBatch, searchSettings);
            this.urlBuilder.fetch(function(data) {
                if (pageNum == -1) {
                    batchPage = data.page;
                }
                this.pageBatch.setItems(batchPage, data.predictions, true);
                if (pageNum == -1) {
                    pageNum = this.pageBatch.getEndPage();
                }
                onData(this.pageBatch.getItems(pageNum), pageNum, true, data.warning);
            }.bind(this), onError);
        }
    }

    saveSearchSettings(searchSettings) {
        let searchSettingsStr = JSON.stringify(searchSettings);
        if (this.lastSearchSettingsStr && searchSettingsStr !== this.lastSearchSettingsStr) {
            this.pageBatch.clearData();
        }
        this.lastSearchSettingsStr = searchSettingsStr;
    }

    setBuilderURL(page, perPage, searchSettings) {
        let urlBuilder = this.urlBuilder;
        urlBuilder.reset(URL.genomes + '/');
        urlBuilder.append(searchSettings.genome);
        urlBuilder.append('/prediction');
        urlBuilder.appendParam('protein', searchSettings.model);
        urlBuilder.appendParam('geneList', searchSettings.geneList);
        urlBuilder.appendParam('customListData', searchSettings.customListData);
        urlBuilder.appendParam('customListFilter', searchSettings.customListFilter, true);
        urlBuilder.appendParam('upstream', searchSettings.upstream);
        urlBuilder.appendParam('downstream', searchSettings.downstream);
        urlBuilder.appendParam('includeAll', searchSettings.all);
        urlBuilder.appendParam('maxPredictionSort', searchSettings.maxPredictionSort);

        if (searchSettings.maxPredictionSort) {
            urlBuilder.appendParam('maxPredictionGuess', '0.4');
        }
        if (page && perPage) {
            urlBuilder.appendParam('page', page);
            urlBuilder.appendParam('perPage', perPage);
        }
    }

    getDownloadURL(format, searchSettings) {
        this.setBuilderURL(undefined, undefined, searchSettings)
        this.urlBuilder.appendParam('format',format);
        return this.urlBuilder.url;
    }

    addLocalUrl(urlBuilder, page, searchSettings) {
        urlBuilder.reset('');
        urlBuilder.appendParam('genome', searchSettings.genome);
        urlBuilder.appendParam('model', searchSettings.model);
        urlBuilder.appendParam('geneList', searchSettings.geneList);
        urlBuilder.appendParam('upstream', searchSettings.upstream);
        urlBuilder.appendParam('downstream', searchSettings.downstream);
        urlBuilder.appendParam('all', searchSettings.all);
        urlBuilder.appendParam('maxPredictionSort', searchSettings.maxPredictionSort);
        urlBuilder.appendParam('customListFilter', searchSettings.customListFilter, true);
        urlBuilder.appendParam('customListData', searchSettings.customListData, true);
    }

}

export default PredictionsStore;