/* jshint esversion: 11, node: true */
// Code to allow Jest to work with jQuery
const $ = require('jquery');
global.$ = global.jQuery = $;

const generateToast = require('./notifications');

describe("generateToast function works correctly", () => {
    test('should generate debug toast template with correct message, tag and delay', () => {
        expect(generateToast('debug', 'debug message', 1)).toEqual(expect.stringContaining('toast-debug'));
        expect(generateToast('debug', 'debug message', 1)).toEqual(expect.stringContaining('debug message'));
        expect(generateToast('debug', 'debug message', 1)).toEqual(expect.stringContaining("data-bs-autohide='false'"));
    });
    test('should generate info toast template with correct message, tag and delay', () => {
        expect(generateToast('info', 'info message', 1)).toEqual(expect.stringContaining('toast-info'));
        expect(generateToast('info', 'info message', 1)).toEqual(expect.stringContaining('info message'));
        expect(generateToast('info', 'info message', 1)).toEqual(expect.stringContaining("data-bs-delay='10000'"));
    });
    test('should generate success toast template with correct message, tag and delay', () => {
        expect(generateToast('success', 'success message', 1)).toEqual(expect.stringContaining('toast-success'));
        expect(generateToast('success', 'success message', 1)).toEqual(expect.stringContaining('success message'));
        expect(generateToast('success', 'success message', 1)).toEqual(expect.stringContaining("data-bs-delay='10000'"));
    });
    test('should generate warning toast template with correct message, tag and delay', () => {
        expect(generateToast('warning', 'warning message', 1)).toEqual(expect.stringContaining('toast-warning'));
        expect(generateToast('warning', 'warning message', 1)).toEqual(expect.stringContaining('warning message'));
        expect(generateToast('warning', 'warning message', 1)).toEqual(expect.stringContaining("data-bs-delay='10000'"));
    });
    test('should generate error toast template with correct message, tag and delay', () => {
        expect(generateToast('error', 'error message', 1)).toEqual(expect.stringContaining('toast-error'));
        expect(generateToast('error', 'error message', 1)).toEqual(expect.stringContaining('error message'));
        expect(generateToast('error', 'error message', 1)).toEqual(expect.stringContaining("data-bs-delay='10000'"));
    });
});