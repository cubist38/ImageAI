import React from "react";
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import Divider from '@mui/material/Divider';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import Typography from '@mui/material/Typography';

const Caption = ({ caption }) => {
    var listCaps = caption.split(",");

    return (
        <>
        <Typography variant="h5">Generated caption</Typography>
        <List sx={{ width: '100%', maxWidth: 500, bgcolor: 'background.paper' }}>
                {listCaps.map((cap, index) => (
                    <>
                    <ListItem alignItems="flex-start">
                        {/* <ListItemAvatar>
                            <Avatar alt={cap} src="/static/images/avatar/1.jpg" />
                        </ListItemAvatar> */}
                        <ListItemText primary={cap}/>
                    </ListItem>
                    <Divider variant="inset" component="li" />
                    </>    
                ))}
        </List>
        </>
    );
}

export default Caption;