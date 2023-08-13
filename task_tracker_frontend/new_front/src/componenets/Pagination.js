import React from "react";

export default function Pagination({fetchNext}) {
    return (
        <nav aria-label="Пример навигации по страницам">
            <ul className="pagination">
                <li className="page-item">
                    <p className="page-link" onClick={fetchNext}>Дальше</p>
                </li>
            </ul>
        </nav>
    );
}
