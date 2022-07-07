/* jshint esversion: 11, node: true */
// Code to allow Jest to work with jQuery
const $ = require('jquery');
global.$ = global.jQuery = $;

beforeAll(() => {
    document.body.innerHTML =
        '<img id="product-image" src="">' +
        '<img id="drawing-overlay" src="">' +
        '<form id="add-to-cart">' +
        '<select id="drawing"></select>' +
        '<select id="variant"></select>' +
        '</form>' +
        '<script id="jsonData" type = "application/json" >{}</script>';
});

describe('positionOverlay function works correctly', () => {
    test('should set drawing-overlay width property', () => {
        const {
            positionOverlay
        } = require('./prints');
        positionOverlay(['10%', '20%', '30%']);
        expect(document.getElementById('drawing-overlay').style.width).toMatch('10%');
    });
    test('should set drawing-overlay left property', () => {
        const {
            positionOverlay
        } = require('./prints');
        positionOverlay(['10%', '20%', '30%']);
        expect(document.getElementById('drawing-overlay').style.left).toMatch('20%');
    });
    test('should set drawing-overlay top property', () => {
        const {
            positionOverlay
        } = require('./prints');
        positionOverlay(['10%', '20%', '30%']);
        expect(document.getElementById('drawing-overlay').style.top).toMatch('30%');
    });
});

describe('setOverlay function works correctly', () => {
    test('should set src of drawing-overlay element', () => {
        const {
            setOverlay
        } = require('./prints');
        setOverlay('drawing-overlay.jpg');
        expect(document.getElementById('drawing-overlay').src).toMatch('drawing-overlay.jpg');
    });
});

describe('setProductImage function works correctly', () => {
    test('should set src of product-image element', () => {
        const {
            setProductImage
        } = require('./prints');
        setProductImage('product-image.jpg');
        expect(document.getElementById('product-image').src).toMatch('product-image.jpg');
    });
});