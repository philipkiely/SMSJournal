function changeCard(token){
    var handler = StripeCheckout.configure({
    key: token,
    image: '/static/undraw_credit_card_df1m.png',
    locale: 'auto',
    panelLabel: "Submit",
    email: user_email,
    token: function(tkn) {
      $.ajax({
            type: 'POST',
            url: url_change,
            data: {"stripeToken":tkn.id, "username":username },
            dataType: "json",
            success: function(resultData) {
              if (resultData["Result"] != "Done" ){
                alert("Something went wrong! Please try again or contact info@grammiegram.com for support.")
              }
            }
      });
    }
  });

  document.getElementById('customButton').addEventListener('click', function(e) {
    handler.open({
      name: 'SMS journal',
      description: 'Change your payment method',
    });
    e.preventDefault();
  });

  window.addEventListener('popstate', function() {
    handler.close();
  });
}
