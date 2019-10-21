import React from "react";
import axios from "axios";
import { connect } from "react-redux";
import { Button, Card } from "antd";
import CustomForm from "../components/Form";


class ArticleDetail extends React.Component {
  state = {
    article: {}
  };



  componentWillReceiveProps(newProps) {
    console.log(newProps);
    if (newProps.token) {

      axios.defaults.headers = {
        "Content-Type": "application/json",
        Authorization: newProps.token
      }
      const articleID = this.props.match.params.articleID;

      axios.get(`http://127.0.0.1:8000/api/${articleID}`).then(res => {
        this.setState({
          article: res.data
        });
      });
    }
  }



  handleDelete = (event) => {

    if (this.props.token !== null) {

      const articleID = this.props.match.params.articleID;
      axios.defaults.headers = {
        "Content-Type": "application/json",
        Authorization: this.props.token
      }
      axios.delete(`http://127.0.0.1:8000/api/${articleID}/delete/`)
      this.props.history.push(`/`);
      this.forceUpdate();

    }
  }


  handleJob = event => {
    event.preventDefault();
    const articleID = this.props.match.params.articleID;
    axios.defaults.headers = {
      "Content-Type": "application/json",
      Authorization: `Token ${this.props.token}`
    };
    axios.get(`http://127.0.0.1:8000/api/${articleID}/job_status_update/`).then(res => {
      this.setState({
        article: res.data
      });
      this.props.history.push(`/`);
      this.forceUpdate()

    });


  };


  renderElement() {
    if (this.state.article.display_text === 'Accept Job')
      return <form onSubmit={this.handleJob}>
        <Button type="primary" htmlType="submit">Accept Job</Button>
      </form>;

    else if (this.state.article.display_text === 'Complete Job')
      return <form onSubmit={this.handleJob}>
        <Button type="primary" htmlType="submit">Complete Job</Button>
      </form>;

    else
      return <p>{this.state.article.display_text} </p>





  }



  render() {
    return (
      <div>

        <Card title={this.state.article.title}>
          <p> {this.state.article.content} </p>
          <p> {this.state.article.budget} </p>

        </Card>

        <br />



        {this.renderElement()}



        <CustomForm
          {...this.props}
          token={this.props.token}
          requestType="put"
          articleID={this.props.match.params.articleID}
          btnText="Update"
        />

        <form onSubmit={this.handleDelete}>
          <Button type="danger" htmlType="submit">
            Delete
                </Button>
        </form>
      </div>

    );
  }
}

const mapStateToProps = state => {
  return {
    token: state.token
  };
};


export default connect(mapStateToProps)(ArticleDetail);
