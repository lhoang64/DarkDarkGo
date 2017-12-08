
exports = Snippet = (id, title, href, desc) => {
    this.id = id
    this.title = title
    this.href = href
    this.desc = desc
}

Snippet.prototype.length = () => String(id).length + title.length + href.length + desc.length + 8
