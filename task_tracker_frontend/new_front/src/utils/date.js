export default function toDateToShow(iso_string_datetime) {
    let date = new Date(iso_string_datetime)
    return date.toLocaleDateString();
}
