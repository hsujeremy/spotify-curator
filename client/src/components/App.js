import React, { Component } from 'react';


class App extends Component {
    constructor(props) {
        super(props);
        this.state = { value: '' };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(e) {
        this.setState({ value: e.target.value });
    }

    handleSubmit(e) {
        e.preventDefault();
        window.location.href = 'http://127.0.0.1:5000/login';
        // Need to figure out how to get state to remain constant
        // Perhaps send it to the store
        sessionStorage.setItem('loggedIn', true);
    }

    // Currently, I can't find any way for the server to send something back to the client verifying the auth was successful
    // Since we are simply redirecting both ways rather than making an HTTP request
    // For now, we assume that if we redirect back here, the authorization was successful
    render() {
        if (sessionStorage.getItem('loggedIn') !== undefined && sessionStorage.getItem('loggedIn'))
            return (
                <div>
                    <h1>User Input Form</h1>
                    <label>Song:
                        <input type='text' value={this.state.value} onChange={this.handleChange} />
                    </label>
                </div>
            );
        return <button onClick={this.handleSubmit}>Login with Spotify</button>;
    }
}

export default App;