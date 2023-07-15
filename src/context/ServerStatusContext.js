import React, { createContext, useState } from "react";

export const ServerStatusContext = createContext();

const ServerStatusContextProvider = props => {
    const [processing, setProcessing] = useState(false);

    return (
        <ServerStatusContext.Provider value= {{ processing, setProcessing }}>
            {props.children}
        </ServerStatusContext.Provider>
    );
};

export default ServerStatusContextProvider;