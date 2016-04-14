// run: ./node_modules/.bin/babel-node jstests/testURLBuilder.jsx
import URLBuilder from './../src/app/store/URLBuilder.jsx';

const assert = require('chai').assert;
var good_ajax_response = true;

function testBuildingPredictionURL() {
    var builder = new URLBuilder(fake_ajax);
    builder.reset('/api/v1/genomes/');
    assert.equal(builder.url, '/api/v1/genomes/');
    builder.append('hg18');
    builder.append('/prediction');
    assert.equal(builder.url, '/api/v1/genomes/hg18/prediction');
    builder.appendParam('protein', 'E2F1');
    assert.equal(builder.url, '/api/v1/genomes/hg18/prediction?protein=E2F1');
    builder.appendParam('gene_list', 'knowngene');
    assert.equal(builder.url, '/api/v1/genomes/hg18/prediction?protein=E2F1&gene_list=knowngene');
    builder.appendParam('page', '1');
    assert.equal(builder.url, '/api/v1/genomes/hg18/prediction?protein=E2F1&gene_list=knowngene&page=1');
    good_ajax_response = true;
    var goodCalled = false;
    builder.fetch(function(data) {
        goodCalled = true;
    }, function(data) {
        assert.fail('Shouldnt get here');
    })
    assert.equal(goodCalled, true, 'We had good called.');

    good_ajax_response = false;
    var badCalled = false;
    builder.fetch(function(data) {
        assert.fail('Shouldnt get here');
    }, function(data) {
        badCalled = true;
    })
    assert.equal(badCalled, true, 'We had good bad.');

}

function fake_ajax(fetchData) {
    if (good_ajax_response) {
        fetchData.success([1,2,3]);
    } else {
        fetchData.error('someurl', 500, 'hey');
    }
}

testBuildingPredictionURL();