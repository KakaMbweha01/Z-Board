import React, { useEffect, useState } from 'react';
import axios from 'axios';

const NoticeList = () => {
    const [notices, setNotices] = useState([]);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/notices')
            .then(response => {
                setNotices(response.data);
            })
            .catch(error => {
                console.error("There was an error fetching the noices!", error);
            });
    }, []);

    return (
        <div>
            <h1>The Noticeboard</h1>
            <ul>
                {notices.map(notice => (
                    <li key={notice.id}>
                        <h2>{notice.title}</h2>
                        <p>{notice.content}</p>
                        <small>Posted by {notice.author} on {notice.date_posted}</small>
                    </li>
                ))}
            </ul>
        </div>
    )

}

export default NoticeList;