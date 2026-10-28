export const TYPE_LABEL = { which_chapter: 'Which chapter', which_section: 'Which section', who_said: 'Who said', context: 'Context', ot_passage: 'Old Testament quote', fill_blank: 'Fill in the blank' };

// The three parts of Galatians, used for the section filter (chapter ranges) and the Index.
export const SECTIONS = [[1, 2, 'Personal defense (1-2)'], [3, 4, 'Doctrinal argument (3-4)'], [5, 6, 'Practical living (5-6)']];

export const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

export const pct = (a, b) => (b ? Math.round((100 * a) / b) : 0);
