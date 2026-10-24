/**
 * Prepal Client-Friendly WYSIWYG Editor
 * Built for educational business owners and content managers.
 * Provides visual rich-text authoring with client-side paste sanitization
 * compatible with Prepal's server-side nh3 whitelist.
 */
(function () {
  'use strict';

  const ALLOWED_TAGS = new Set([
    'h2', 'h3', 'h4', 'p', 'br', 'hr', 'strong', 'em', 'b', 'i', 'u', 's',
    'blockquote', 'ul', 'ol', 'li', 'a', 'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td'
  ]);

  function sanitizeHtmlString(html) {
    if (!html) return '';
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');

    function cleanNode(node) {
      if (node.nodeType === Node.TEXT_NODE) {
        return document.createTextNode(node.textContent);
      }
      if (node.nodeType !== Node.ELEMENT_NODE) {
        return null;
      }

      const tagName = node.tagName.toLowerCase();
      if (!ALLOWED_TAGS.has(tagName)) {
        // Unwrap disallowed tags: keep text/allowed children
        const frag = document.createDocumentFragment();
        node.childNodes.forEach((child) => {
          const cleanedChild = cleanNode(child);
          if (cleanedChild) frag.appendChild(cleanedChild);
        });
        return frag;
      }

      const cleanEl = document.createElement(tagName);
      // Copy allowed attributes only
      if (tagName === 'a') {
        const href = node.getAttribute('href') || '';
        if (/^(https?:|mailto:|\/|#)/i.test(href)) {
          cleanEl.setAttribute('href', href);
          cleanEl.setAttribute('target', '_blank');
          cleanEl.setAttribute('rel', 'noopener noreferrer');
        }
      }
      if (tagName === 'blockquote' && node.classList.contains('exam-note')) {
        cleanEl.className = 'exam-note';
      }
      if (tagName === 'th' || tagName === 'td') {
        const colspan = node.getAttribute('colspan');
        const rowspan = node.getAttribute('rowspan');
        if (colspan && /^\d+$/.test(colspan)) cleanEl.setAttribute('colspan', colspan);
        if (rowspan && /^\d+$/.test(rowspan)) cleanEl.setAttribute('rowspan', rowspan);
      }

      node.childNodes.forEach((child) => {
        const cleanedChild = cleanNode(child);
        if (cleanedChild) cleanEl.appendChild(cleanedChild);
      });
      return cleanEl;
    }

    const frag = document.createDocumentFragment();
    doc.body.childNodes.forEach((child) => {
      const cleaned = cleanNode(child);
      if (cleaned) frag.appendChild(cleaned);
    });

    const wrapper = document.createElement('div');
    wrapper.appendChild(frag);
    return wrapper.innerHTML;
  }

  function editorValue(editor) {
    // Browser placeholder markup must not turn an untouched extra Django inline
    // into a changed (and invalid) new content block on every form submission.
    if (!editor.textContent.trim() && !editor.querySelector('table,hr,figure,pre,code')) return '';
    return editor.innerHTML;
  }

  function createToolbar(editor, textarea, updateMode) {
    const toolbar = document.createElement('div');
    toolbar.className = 'prepal-wysiwyg-toolbar';

    function createBtn(label, title, command, arg = null) {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'prepal-tb-btn';
      btn.innerHTML = label;
      btn.title = title;
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        editor.focus();
        if (typeof command === 'function') {
          command();
        } else {
          document.execCommand(command, false, arg);
        }
        syncToTextarea();
      });
      return btn;
    }

    function createFormatSelect() {
      const select = document.createElement('select');
      select.className = 'prepal-tb-select';
      select.title = 'Formatting block';
      const options = [
        { val: 'p', label: 'Paragraph (Normal)' },
        { val: 'h2', label: 'Heading 2 (Major Section)' },
        { val: 'h3', label: 'Heading 3 (Sub-section)' },
      ];
      options.forEach((opt) => {
        const o = document.createElement('option');
        o.value = opt.val;
        o.textContent = opt.label;
        select.appendChild(o);
      });
      select.addEventListener('change', () => {
        editor.focus();
        document.execCommand('formatBlock', false, `<${select.value}>`);
        syncToTextarea();
      });
      return select;
    }

    function syncToTextarea() {
      textarea.value = editorValue(editor);
      textarea.dispatchEvent(new Event('input', { bubbles: true }));
    }

    // Format Block dropdown
    toolbar.appendChild(createFormatSelect());

    // Basic formatting
    toolbar.appendChild(createBtn('<b>B</b>', 'Bold (Ctrl+B)', 'bold'));
    toolbar.appendChild(createBtn('<i>I</i>', 'Italic (Ctrl+I)', 'italic'));
    toolbar.appendChild(createBtn('<u>U</u>', 'Underline (Ctrl+U)', 'underline'));

    // Divider
    const sep1 = document.createElement('span');
    sep1.className = 'prepal-tb-sep';
    toolbar.appendChild(sep1);

    // Lists
    toolbar.appendChild(createBtn('• List', 'Bullet List', 'insertUnorderedList'));
    toolbar.appendChild(createBtn('1. List', 'Numbered List', 'insertOrderedList'));

    // Quote / Callout
    toolbar.appendChild(createBtn('“ Quote', 'Quote / Definition', 'formatBlock', '<blockquote>'));
    toolbar.appendChild(createBtn('💡 Key Point', 'Insert Exam Key Point Box', () => {
      const noteHtml = '<blockquote class="exam-note"><strong>📌 Key Exam Point:</strong> Enter essential takeaway or historical fact here.</blockquote><p><br></p>';
      document.execCommand('insertHTML', false, noteHtml);
    }));

    // Divider
    const sep2 = document.createElement('span');
    sep2.className = 'prepal-tb-sep';
    toolbar.appendChild(sep2);

    // Table insertion
    toolbar.appendChild(createBtn('📊 Table', 'Insert Educational Comparison Table', () => {
      const tableHtml = `
        <table class="educational-table" style="width:100%; border-collapse: collapse; margin: 12px 0;">
          <thead>
            <tr>
              <th style="border: 1px solid #ccc; padding: 8px; background: rgba(0,0,0,0.04);">Category / Site</th>
              <th style="border: 1px solid #ccc; padding: 8px; background: rgba(0,0,0,0.04);">Key Details & Evidence</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="border: 1px solid #ccc; padding: 8px;">Example 1</td>
              <td style="border: 1px solid #ccc; padding: 8px;">Details here...</td>
            </tr>
            <tr>
              <td style="border: 1px solid #ccc; padding: 8px;">Example 2</td>
              <td style="border: 1px solid #ccc; padding: 8px;">Details here...</td>
            </tr>
          </tbody>
        </table>
        <p><br></p>
      `;
      document.execCommand('insertHTML', false, tableHtml);
    }));

    // Link
    toolbar.appendChild(createBtn('🔗 Link', 'Insert Web Link', () => {
      const url = prompt('Enter URL (https://...):', 'https://');
      if (url && /^(https?:|mailto:)/i.test(url)) {
        document.execCommand('createLink', false, url);
      }
    }));

    // Divider
    const sep3 = document.createElement('span');
    sep3.className = 'prepal-tb-sep';
    toolbar.appendChild(sep3);

    // Source code toggle
    let isHtmlMode = false;
    const modeBtn = createBtn('</> Code', 'Toggle HTML Source View', () => {
      isHtmlMode = !isHtmlMode;
      if (isHtmlMode) {
        textarea.value = editorValue(editor);
        textarea.style.display = 'block';
        editor.style.display = 'none';
        modeBtn.classList.add('active');
        modeBtn.innerHTML = '👁️ Visual';
      } else {
        editor.innerHTML = sanitizeHtmlString(textarea.value);
        textarea.style.display = 'none';
        editor.style.display = 'block';
        modeBtn.classList.remove('active');
        modeBtn.innerHTML = '</> Code';
      }
    });
    toolbar.appendChild(modeBtn);

    return toolbar;
  }

  function initWysiwygForTextarea(textarea) {
    if (textarea.dataset.prepalWysiwygInitialized) return;
    textarea.dataset.prepalWysiwygInitialized = 'true';

    // Container wrapper
    const container = document.createElement('div');
    container.className = 'prepal-wysiwyg-container';

    // Editable canvas
    const editor = document.createElement('div');
    editor.className = 'prepal-wysiwyg-editor';
    editor.contentEditable = 'true';
    editor.innerHTML = sanitizeHtmlString(textarea.value || '<p><br></p>');

    // Toolbar
    const toolbar = createToolbar(editor, textarea);

    // Hide original textarea
    textarea.style.display = 'none';
    textarea.parentNode.insertBefore(container, textarea);
    container.appendChild(toolbar);
    container.appendChild(editor);
    container.appendChild(textarea);

    // Sync from editor to textarea on input / blur
    function sync() {
      textarea.value = editorValue(editor);
    }
    editor.addEventListener('input', sync);
    editor.addEventListener('blur', sync);

    // Paste interception with client-side sanitization
    editor.addEventListener('paste', (e) => {
      e.preventDefault();
      const clipboardData = e.clipboardData || window.clipboardData;
      let pastedData = clipboardData.getData('text/html');
      if (!pastedData) {
        // Plain text paste: convert newlines to paragraphs
        const text = clipboardData.getData('text/plain') || '';
        pastedData = text
          .split(/\n\n+/)
          .map((p) => `<p>${p.replace(/\n/g, '<br>')}</p>`)
          .join('');
      }
      const clean = sanitizeHtmlString(pastedData);
      document.execCommand('insertHTML', false, clean);
      sync();
    });

    // Ensure form submission sends the latest editor value
    const form = textarea.closest('form');
    if (form && !form.dataset.prepalSubmitHooked) {
      form.dataset.prepalSubmitHooked = 'true';
      form.addEventListener('submit', () => {
        document.querySelectorAll('.prepal-wysiwyg-editor').forEach((ed) => {
          const ta = ed.parentNode.querySelector('textarea');
          if (ta && ed.style.display !== 'none') {
            ta.value = editorValue(ed);
          }
        });
      });
    }
  }

  // Reactive toggling based on ContentBlock type (text vs image vs heading)
  function setupBlockTypeToggle(inlineRow) {
    const blockTypeSelect = inlineRow.querySelector('select[name$="-block_type"]');
    if (!blockTypeSelect) return;

    function applyVisibility() {
      const val = blockTypeSelect.value;
      const fileRow = inlineRow.querySelector('.field-file');
      const altRow = inlineRow.querySelector('.field-alt_text');
      const captionRow = inlineRow.querySelector('.field-caption');
      const contentRow = inlineRow.querySelector('.field-content');

      if (val === 'image') {
        if (fileRow) fileRow.style.display = '';
        if (altRow) altRow.style.display = '';
        if (captionRow) captionRow.style.display = '';
        // Image doesn't require rich-text body, keep content minimal or optional
        if (contentRow) {
          const ed = contentRow.querySelector('.prepal-wysiwyg-container');
          if (ed) ed.style.display = 'none';
        }
      } else {
        if (fileRow) fileRow.style.display = 'none';
        if (altRow) altRow.style.display = 'none';
        if (captionRow) captionRow.style.display = 'none';
        if (contentRow) {
          const ed = contentRow.querySelector('.prepal-wysiwyg-container');
          if (ed) ed.style.display = '';
        }
      }
    }

    blockTypeSelect.addEventListener('change', applyVisibility);
    applyVisibility();
  }

  function initAll() {
    // Find all textareas intended for WYSIWYG
    document.querySelectorAll('.prepal-wysiwyg-textarea, textarea[name$="-content"]').forEach((ta) => {
      initWysiwygForTextarea(ta);
    });

    // Setup block type toggling for inline blocks
    document.querySelectorAll('.inline-related').forEach((inlineRow) => {
      setupBlockTypeToggle(inlineRow);
    });
  }

  // Initialize on DOMContentLoaded and on dynamic inline additions
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }

  // Hook into Django inline addition event
  document.addEventListener('formset:added', (event) => {
    const newRow = event.target;
    if (newRow) {
      newRow.querySelectorAll('textarea[name$="-content"]').forEach((ta) => {
        initWysiwygForTextarea(ta);
      });
      setupBlockTypeToggle(newRow);
    }
  });
})();
