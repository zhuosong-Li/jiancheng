export const handleRowClick = (row) => {
    let url = ""
    const queryString = new URLSearchParams(row).toString();
    if (row.statusId === 20) {
        url = `${window.location.origin}/fabriccutting/pricereport?${queryString}`;
    } else if (row.statusId === 23) {
        url = `${window.location.origin}/fabriccutting/shoetypelist?${queryString}`;
    }
    if (url) {
        window.open(url, '_blank');
    }
}
